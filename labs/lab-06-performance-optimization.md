# Lab 6: Performance Optimization

## 🎯 Learning Objectives

- Understand DuckDB query execution and optimization
- Master indexing strategies for performance
- Optimize memory and thread configuration
- Analyze query plans and bottlenecks
- Implement caching strategies
- Learn lakehouse performance patterns

## 📋 Prerequisites

- Completed Lab 5: Data Format Operations
- Working DuckDB environment
- Sample database loaded
- Understanding of basic SQL operations

## ⏱️ Estimated Time

45-60 minutes

## 🎓 Conceptual Background

Performance optimization is critical for production lakehouse environments. This lab covers:

**Query Execution Plans**: Understanding how DuckDB executes queries
**Indexing Strategies**: When and how to use indexes effectively
**Memory Management**: Optimizing memory usage for large datasets
**Thread Configuration**: Parallel processing optimization
**Caching Strategies**: Reducing redundant computation
**Lakehouse Performance**: Optimizing multi-layer architectures

## 🚀 Step-by-Step Instructions

### Step 1: Query Execution Analysis

Understand how DuckDB executes and optimizes queries.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Basic query execution analysis
print("Query execution analysis...")

# Simple query
query = "SELECT COUNT(*) FROM sample_customers"
result = con.execute(query).fetchone()
print(f"Query result: {result[0]}")

# Query execution plan
print("\nExecution plan:")
plan = con.execute(f"EXPLAIN {query}").fetchall()
for line in plan:
    print(line[0])

# Analyze query performance
import time

start = time.time()
result = con.execute(query).fetchone()
execution_time = time.time() - start
print(f"\nExecution time: {execution_time:.4f} seconds")

# Complex query analysis
complex_query = """
SELECT 
    c.segment,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value
FROM sample_customers c
LEFT JOIN sample_orders o ON c.customer_id = o.customer_id
GROUP BY c.segment
"""

print("\nComplex query analysis:")
start = time.time()
result = con.execute(complex_query).fetchdf()
execution_time = time.time() - start
print(f"Complex query execution time: {execution_time:.4f} seconds")
print("Results:")
print(result)

# Detailed execution plan
print("\nDetailed execution plan:")
detailed_plan = con.execute(f"EXPLAIN ANALYZE {complex_query}").fetchall()
for line in detailed_plan:
    print(line[0])
```

### Step 2: Indexing Strategies

Learn when and how to use indexes effectively.

```python
import duckdb
import time

con = duckdb.connect('data/duckdb_practice.db')

# Create test data for indexing demonstration
print("Creating test data for indexing...")

con.execute("""
    CREATE TABLE IF NOT EXISTS test_customers AS
    SELECT * FROM sample_customers
""")

# Query without index
print("\nQuery without index:")
query = "SELECT * FROM test_customers WHERE segment = 'Premium'"
start = time.time()
result = con.execute(query).fetchdf()
no_index_time = time.time() - start
print(f"Execution time without index: {no_index_time:.4f} seconds")
print(f"Rows returned: {len(result)}")

# Create index
print("\nCreating index on segment...")
con.execute("CREATE INDEX idx_segment ON test_customers(segment)")
print("Index created")

# Query with index
print("\nQuery with index:")
start = time.time()
result = con.execute(query).fetchdf()
with_index_time = time.time() - start
print(f"Execution time with index: {with_index_time:.4f} seconds")
print(f"Performance improvement: {no_index_time / with_index_time:.2f}x")

# Composite index
print("\nCreating composite index...")
con.execute("CREATE INDEX idx_segment_loyalty ON test_customers(segment, loyalty_points)")
print("Composite index created")

# Query using composite index
composite_query = """
    SELECT * FROM test_customers 
    WHERE segment = 'Premium' AND loyalty_points > 5000
"""
start = time.time()
result = con.execute(composite_query).fetchdf()
composite_time = time.time() - start
print(f"Composite index query time: {composite_time:.4f} seconds")

# Index maintenance
print("\nIndex information:")
indexes = con.execute("""
    SELECT index_name, table_name, column_names 
    FROM duckdb_indexes()
""").fetchdf()
print(indexes)

# Drop index if needed
con.execute("DROP INDEX idx_segment")
print("Dropped index")
```

### Step 3: Memory Configuration

Optimize memory settings for your workload.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Check current memory settings
print("Current memory settings:")
memory_settings = con.execute("""
    SELECT name, value 
    FROM duckdb_settings() 
    WHERE name LIKE '%memory%'
""").fetchdf()
print(memory_settings)

# Set memory limit
print("\nSetting memory limit...")
con.execute("SET memory_limit='2GB'")
print("Memory limit set to 2GB")

# Test memory-intensive operations
print("\nMemory-intensive operation test...")

# Large aggregation
large_query = """
SELECT 
    DATE_TRUNC('day', order_date) as day,
    COUNT(*) as orders,
    SUM(total_amount) as revenue,
    COUNT(DISTINCT customer_id) as customers
FROM sample_orders
GROUP BY day
ORDER BY day
"""

start = time.time()
result = con.execute(large_query).fetchdf()
execution_time = time.time() - start
print(f"Large aggregation time: {execution_time:.4f} seconds")
print(f"Results: {len(result)} days")

# Memory profiling
print("\nMemory profiling...")
con.execute("SET enable_memory_profiling=true")

# Run query with profiling
con.execute("SET enable_profiling=true")
profiling_result = con.execute("SELECT * FROM sample_customers LIMIT 1000").fetchdf()
print(f"Profiling query completed: {len(profiling_result)} rows")

# Check memory usage
try:
    memory_info = con.execute("SELECT * FROM duckdb_memory_info()").fetchdf()
    print("Memory usage information:")
    print(memory_info)
except:
    print("Memory profiling not available in this version")

# Optimize for different memory scenarios
print("\nMemory optimization strategies...")

# For low memory environments
con.execute("SET memory_limit='512MB'")
con.execute("SET enable_object_cache=false")
print("Low memory configuration applied")

# For high memory environments
con.execute("SET memory_limit='8GB'")
con.execute("SET enable_object_cache=true")
print("High memory configuration applied")
```

### Step 4: Thread Configuration

Optimize parallel processing for your hardware.

```python
import duckdb
import time

con = duckdb.connect('data/duckdb_practice.db')

# Check current thread settings
print("Current thread settings:")
thread_settings = con.execute("""
    SELECT name, value 
    FROM duckdb_settings() 
    WHERE name LIKE '%thread%'
""").fetchdf()
print(thread_settings)

# Test different thread configurations
print("\nThread configuration testing...")

query = """
SELECT 
    segment,
    COUNT(*) as customer_count,
    AVG(loyalty_points) as avg_loyalty,
    STDDEV(loyalty_points) as std_loyalty
FROM sample_customers
GROUP BY segment
"""

thread_counts = [1, 2, 4, 8]
results = []

for thread_count in thread_counts:
    con.execute(f"SET threads={thread_count}")
    
    start = time.time()
    result = con.execute(query).fetchdf()
    execution_time = time.time() - start
    
    results.append({
        'threads': thread_count,
        'time': execution_time,
        'speedup': results[0]['time'] / execution_time if results else 1.0
    })
    
    print(f"Threads: {thread_count}, Time: {execution_time:.4f}s, Speedup: {results[-1]['speedup']:.2f}x")

# Optimal thread configuration
print("\nOptimal thread analysis:")
best_config = max(results, key=lambda x: x['speedup'])
print(f"Best configuration: {best_config['threads']} threads")
print(f"Speedup: {best_config['speedup']:.2f}x")

# Set optimal configuration
con.execute(f"SET threads={best_config['threads']}")
print(f"Set optimal thread count: {best_config['threads']}")
```

### Step 5: Caching Strategies

Implement caching to reduce redundant computation.

```python
import duckdb
import time

con = duckdb.connect('data/duckdb_practice.db')

# Enable caching
print("Enabling caching...")
con.execute("SET enable_object_cache=true")
con.execute("SET enable_progress_bar=true")
print("Caching enabled")

# Test query caching
print("\nQuery caching test...")

expensive_query = """
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value
FROM sample_customers c
LEFT JOIN sample_orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 0
"""

# First execution (cache miss)
start = time.time()
result1 = con.execute(expensive_query).fetchdf()
first_execution = time.time() - start
print(f"First execution (cache miss): {first_execution:.4f}s")

# Second execution (cache hit)
start = time.time()
result2 = con.execute(expensive_query).fetchdf()
second_execution = time.time() - start
print(f"Second execution (cache hit): {second_execution:.4f}s")
print(f"Cache speedup: {first_execution / second_execution:.2f}x")

# Result caching
print("\nResult caching test...")

# Cache result explicitly
con.execute("PRAGMA enable_cache=true")

# Materialized view pattern
print("\nMaterialized view pattern...")

# Create materialized view
con.execute("""
    CREATE OR REPLACE VIEW mv_customer_summary AS
    SELECT 
        customer_id,
        first_name,
        last_name,
        segment,
        loyalty_points
    FROM sample_customers
    WHERE is_active = true
""")

# Query materialized view
start = time.time()
mv_result = con.execute("SELECT * FROM mv_customer_summary").fetchdf()
mv_time = time.time() - start
print(f"Materialized view query: {mv_time:.4f}s")

# Cache invalidation
print("\nCache management...")

# Clear cache
con.execute("PRAGMA clear_cache")
print("Cache cleared")

# Check cache status
try:
    cache_info = con.execute("SELECT * FROM duckdb_cache_info()").fetchdf()
    print("Cache information:")
    print(cache_info)
except:
    print("Cache information not available in this version")
```

### Step 6: Lakehouse Performance Optimization

Optimize performance across lakehouse layers.

```python
import duckdb
import time

con = duckdb.connect('data/duckdb_practice.db')

# Lakehouse layer performance
print("Lakehouse layer performance analysis...")

# Bronze layer performance
print("\nBronze layer (raw data):")
bronze_query = "SELECT COUNT(*) FROM sample_orders"
start = time.time()
bronze_result = con.execute(bronze_query).fetchone()
bronze_time = time.time() - start
print(f"Bronze layer query: {bronze_time:.4f}s")

# Silver layer performance (with filtering)
print("\nSilver layer (filtered data):")
silver_query = """
SELECT COUNT(*) FROM sample_orders 
WHERE order_date >= '2022-01-01' AND status = 'delivered'
"""
start = time.time()
silver_result = con.execute(silver_query).fetchone()
silver_time = time.time() - start
print(f"Silver layer query: {silver_time:.4f}s")

# Gold layer performance (aggregated)
print("\nGold layer (aggregated data):")
gold_query = """
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
FROM sample_orders
WHERE order_date >= '2022-01-01'
GROUP BY month
"""
start = time.time()
gold_result = con.execute(gold_query).fetchdf()
gold_time = time.time() - start
print(f"Gold layer query: {gold_time:.4f}s")

# Performance comparison
print("\nLayer performance comparison:")
print(f"Bronze: {bronze_time:.4f}s")
print(f"Silver: {silver_time:.4f}s (vs Bronze: {bronze_time/silver_time:.2f}x)")
print(f"Gold: {gold_time:.4f}s (vs Bronze: {bronze_time/gold_time:.2f}x)")

# Partition pruning optimization
print("\nPartition pruning simulation...")

# Create partitioned-like structure
con.execute("""
    CREATE OR REPLACE TABLE orders_2022 AS
    SELECT * FROM sample_orders 
    WHERE order_date >= '2022-01-01' AND order_date < '2023-01-01'
""")

con.execute("""
    CREATE OR REPLACE TABLE orders_2023 AS
    SELECT * FROM sample_orders 
    WHERE order_date >= '2023-01-01'
""")

# Query with partition pruning
partitioned_query = """
SELECT COUNT(*) FROM orders_2022 
WHERE order_date >= '2022-06-01'
"""
start = time.time()
partitioned_result = con.execute(partitioned_query).fetchone()
partitioned_time = time.time() - start
print(f"Partitioned query: {partitioned_time:.4f}s")

# Column pruning optimization
print("\nColumn pruning optimization...")

# Query all columns
all_columns = "SELECT * FROM sample_customers LIMIT 10000"
start = time.time()
all_result = con.execute(all_columns).fetchdf()
all_time = time.time() - start
print(f"All columns query: {all_time:.4f}s")

# Query specific columns
specific_columns = "SELECT customer_id, first_name, segment FROM sample_customers LIMIT 10000"
start = time.time()
specific_result = con.execute(specific_columns).fetchdf()
specific_time = time.time() - start
print(f"Specific columns query: {specific_time:.4f}s")
print(f"Column pruning benefit: {all_time/specific_time:.2f}x")

# Performance monitoring
print("\nPerformance monitoring setup...")

# Enable query profiling
con.execute("SET enable_profiling=true")
con.execute("SET enable_optimizer=true")

# Create performance monitoring view
con.execute("""
    CREATE OR REPLACE VIEW performance_log AS
    SELECT 
        query,
        execution_time,
        rows_processed
    -- This would be populated by your monitoring system
""")

print("Performance monitoring infrastructure ready")
```

## 💻 Hands-On Exercises

### Exercise 1: Query Optimization Challenge

Optimize a set of poorly performing queries:

```python
# Your code here
# Analyze query plans
# Identify bottlenecks
# Apply optimization techniques
# Measure improvements
# Document best practices
```

### Exercise 2: Index Strategy Design

Design and implement comprehensive indexing strategy:

```python
# Your code here
# Analyze query patterns
# Design appropriate indexes
# Implement composite indexes
# Monitor index performance
# Balance read vs write performance
```

### Exercise 3: Memory Optimization

Optimize memory usage for large dataset processing:

```python
# Your code here
# Profile memory usage
# Implement memory-efficient algorithms
# Configure memory settings
# Handle out-of-memory scenarios
# Optimize data structures
```

### Exercise 4: Parallel Processing Optimization

Maximize parallel processing performance:

```python
# Your code here
# Analyze hardware capabilities
# Optimize thread configuration
# Implement parallel algorithms
# Balance parallelism overhead
# Monitor CPU utilization
```

### Exercise 5: Lakehouse Performance Strategy

Develop comprehensive lakehouse performance strategy:

```python
# Your code here
# Optimize each lakehouse layer
# Implement data skipping
# Design partitioning strategy
# Optimize file formats
# Monitor end-to-end performance
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Understand DuckDB query execution and optimization
2. ✅ Master indexing strategies
3. ✅ Optimize memory and thread configuration
4. ✅ Analyze and improve query performance
5. ✅ Implement effective caching strategies
6. ✅ Optimize lakehouse architecture performance

## 🔍 Verification

Test your performance optimization skills:

```python
import duckdb
import time

con = duckdb.connect('data/duckdb_practice.db')

# Test query optimization
query = "SELECT COUNT(*) FROM sample_customers WHERE segment = 'Premium'"
start = time.time()
result = con.execute(query).fetchone()
query_time = time.time() - start
print(f"Query performance test: {query_time:.4f}s")

# Test indexing
con.execute("CREATE INDEX IF NOT EXISTS idx_test ON test_customers(segment)")
print("Indexing test: PASSED")

# Test configuration
con.execute("SET threads=4")
print("Configuration test: PASSED")

print("✅ Performance optimization test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: Queries still slow after optimization

**Solution**: Check for other bottlenecks:
```python
# Check I/O performance
con.execute("SET enable_progress_bar=true")

# Check memory pressure
con.execute("SELECT * FROM duckdb_memory_info()")

# Analyze actual execution plan
con.execute("EXPLAIN ANALYZE <query>")
```

### Issue: Index not being used

**Solution**: Verify index usage and query patterns:
```python
# Check if index exists
con.execute("SELECT * FROM duckdb_indexes()")

# Force index usage
con.execute("SET enable_optimizer=true")

# Check query plan for index usage
con.execute("EXPLAIN <query>")
```

### Issue: Memory exhaustion

**Solution**: Implement memory management strategies:
```python
# Reduce memory limit
con.execute("SET memory_limit='2GB'")

# Process in batches
for batch in con.execute("SELECT * FROM large_table").fetchmany(1000):
    # Process batch
    pass

# Disable object cache
con.execute("SET enable_object_cache=false")
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 7**: Extensions & Advanced Features
2. **Study query optimization**: Deep dive into query planning
3. **Implement monitoring**: Set up production monitoring
4. **Benchmark workloads**: Test with real data patterns

---

**You now have comprehensive performance optimization skills for production lakehouse environments!**