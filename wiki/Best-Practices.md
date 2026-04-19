# Best Practices

Production-ready patterns and best practices for using DuckDB in lakehouse environments.

## 🏗️ Architecture Best Practices

### Lakehouse Layer Design

#### Bronze Layer (Raw Data)
**Purpose**: Ingest raw data without transformation

**Best Practices**:
- Use append-only, immutable storage
- Store data in open formats (Parquet preferred)
- Include metadata (ingestion timestamp, source system)
- Implement data lineage tracking
- Use partitioning for large datasets

```python
# Bronze layer best practice
con.execute("""
    COPY raw_events TO 's3://lakehouse/bronze/events/' 
    (FORMAT PARQUET, PARTITION_BY (DATE_TRUNC('day', event_timestamp)), 
     COMPRESSION 'snappy')
""")
```

#### Silver Layer (Cleaned Data)
**Purpose**: Clean, validate, and standardize data

**Best Practices**:
- Implement comprehensive data validation
- Apply consistent data quality rules
- Use appropriate data types
- Implement deduplication strategies
- Maintain data quality metrics

```python
# Silver layer best practice
con.execute("""
    COPY (
        SELECT 
            event_id,
            customer_id,
            event_timestamp,
            event_type,
            -- Data validation
            CASE 
                WHEN event_timestamp > CURRENT_TIMESTAMP THEN NULL
                ELSE event_timestamp
            END as validated_timestamp,
            -- Quality metrics
            CASE 
                WHEN event_timestamp > CURRENT_TIMESTAMP THEN 0
                ELSE 100
            END as quality_score
        FROM bronze_events
    ) TO 's3://lakehouse/silver/events/' 
    (FORMAT PARQUET, PARTITION_BY (event_type, quality_score))
""")
```

#### Gold Layer (Business-Ready Data)
**Purpose**: Aggregated, business-ready data for analytics

**Best Practices**:
- Pre-compute frequently used aggregations
- Use star/snowflake schemas for BI tools
- Optimize for query performance
- Implement data versioning
- Include business metadata

```python
# Gold layer best practice
con.execute("""
    COPY (
        SELECT 
            DATE_TRUNC('day', event_timestamp) as metric_date,
            event_type,
            COUNT(*) as event_count,
            COUNT(DISTINCT customer_id) as unique_customers,
            AVG(session_duration) as avg_session_duration,
            SUM(revenue) as total_revenue
        FROM silver_events
        WHERE quality_score = 100
        GROUP BY metric_date, event_type
    ) TO 's3://lakehouse/gold/daily_metrics/' 
    (FORMAT PARQUET, COMPRESSION 'zstd')
""")
```

## 🔧 Performance Best Practices

### Query Optimization

#### 1. Use Appropriate Data Types
```python
# Good: Use appropriate types
con.execute("""
    CREATE TABLE orders (
        order_id INTEGER,
        order_date DATE,
        total_amount DECIMAL(15,2),
        status VARCHAR
    )
""")

# Avoid: Generic types when specific ones exist
```

#### 2. Leverage DuckDB's Optimizations
```python
# Enable query optimization
con.execute("SET enable_optimizer=true")
con.execute("SET enable_object_cache=true")

# Use parallel processing
con.execute("SET threads=8")
```

#### 3. Use Column Pruning
```python
# Good: Select specific columns
con.execute("SELECT col1, col2 FROM large_table")

# Avoid: SELECT * when not needed
```

#### 4. Implement Partitioning
```python
# Partition by frequently filtered columns
con.execute("""
    COPY table TO 's3://path/' 
    (FORMAT PARQUET, PARTITION_BY (date_column, category_column))
""")
```

### Memory Management

#### 1. Set Appropriate Memory Limits
```python
# Set based on available system memory
con.execute("SET memory_limit='8GB'")
```

#### 2. Process Large Datasets in Batches
```python
# Process in chunks to avoid memory issues
for chunk in con.execute("SELECT * FROM large_table").fetchmany(10000):
    process_chunk(chunk)
```

#### 3. Use Efficient Data Structures
```python
# Use DuckDB's native operations instead of Python loops
# Good:
result = con.execute("SELECT category, COUNT(*) FROM table GROUP BY category").df()

# Avoid: Row-by-row processing in Python
```

## 🔄 ETL Best Practices

### Pipeline Design

#### 1. Implement Idempotency
```python
# Ensure operations can be safely re-run
con.execute("""
    INSERT OR REPLACE INTO target_table
    SELECT * FROM source_table
    WHERE processing_date = CURRENT_DATE
""")
```

#### 2. Add Comprehensive Error Handling
```python
try:
    con.execute("BEGIN TRANSACTION")
    # ETL operations
    con.execute("COMMIT")
except Exception as e:
    con.execute("ROLLBACK")
    log_error(e)
    raise
```

#### 3. Implement Data Validation
```python
# Validate data quality before loading
validation_query = """
SELECT COUNT(*) - COUNT(DISTINCT id) as duplicates,
       COUNT(*) - COUNT(id) as null_ids
FROM staging_table
"""
validation_result = con.execute(validation_query).fetchone()
if validation_result[0] > 0 or validation_result[1] > 0:
    raise ValueError("Data validation failed")
```

### Data Quality Framework

#### 1. Define Quality Rules
```python
quality_rules = {
    'completeness': 'column IS NOT NULL',
    'uniqueness': 'COUNT(*) = COUNT(DISTINCT column)',
    'validity': 'column IN (valid_values)',
    'timeliness': 'date >= CURRENT_DATE - INTERVAL 30 days'
}
```

#### 2. Implement Automated Validation
```python
def validate_data(table_name, rules):
    for rule_name, rule in rules.items():
        result = con.execute(f"""
            SELECT CASE WHEN {rule} THEN 1 ELSE 0 END as passed
            FROM {table_name}
        """).fetchone()
        if not result[0]:
            log_validation_failure(rule_name, table_name)
```

## 📊 Data Format Best Practices

### Parquet Optimization

#### 1. Choose Appropriate Compression
```python
# Snappy: Balanced performance and compression
con.execute("COPY table TO 'path/' (FORMAT PARQUET, COMPRESSION 'snappy')")

# ZSTD: Maximum compression (slower writes)
con.execute("COPY table TO 'path/' (FORMAT PARQUET, COMPRESSION 'zstd')")

# GZIP: Maximum compatibility
con.execute("COPY table TO 'path/' (FORMAT PARQUET, COMPRESSION 'gzip')")
```

#### 2. Optimize Row Group Size
```python
# Larger row groups for large datasets
con.execute("COPY table TO 'path/' (FORMAT PARQUET, ROW_GROUP_SIZE 1000000)")

# Smaller row groups for frequent queries
con.execute("COPY table TO 'path/' (FORMAT PARQUET, ROW_GROUP_SIZE 100000)")
```

#### 3. Use Dictionary Encoding
```python
# DuckDB automatically uses dictionary encoding for low-cardinality columns
# Ensure columns with few distinct values are used appropriately
```

### Arrow Integration

#### 1. Leverage Zero-Copy Operations
```python
# Zero-copy between DuckDB and Arrow
arrow_table = con.execute("SELECT * FROM table").arrow()

# Register Arrow table for querying
con.register('arrow_table', arrow_table)
```

#### 2. Use Arrow for Interoperability
```python
# Convert between DuckDB and other systems
import pyarrow as pa
import pandas as pd

# DuckDB → Arrow → Pandas
arrow_table = con.execute("SELECT * FROM table").arrow()
df = arrow_table.to_pandas()

# Pandas → Arrow → DuckDB
arrow_table = pa.Table.from_pandas(df)
con.register('pandas_data', arrow_table)
```

## 🔒 Security Best Practices

### Access Control

#### 1. Implement Role-Based Access
```python
# Define user roles
roles = {
    'admin': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
    'analyst': ['SELECT'],
    'writer': ['SELECT', 'INSERT'],
    'reader': ['SELECT']
}

# Grant permissions based on roles
def grant_permissions(user, role):
    for permission in roles[role]:
        con.execute(f"GRANT {permission} ON ALL TABLES IN SCHEMA TO {user}")
```

#### 2. Use Environment Variables for Credentials
```python
# Never hardcode credentials
import os

db_password = os.getenv('DB_PASSWORD')
con = duckdb.connect('database.db', read_only=False)
```

### Data Encryption

#### 1. Encrypt Data at Rest
```python
# Use DuckDB's encryption for sensitive databases
con = duckdb.connect('encrypted.db', key='your-encryption-key')
```

#### 2. Mask Sensitive Data
```python
# Mask sensitive data in queries
con.execute("""
    SELECT 
        customer_id,
        CONCAT(SUBSTRING(email, 1, 3), '***@', SUBSTRING(email, STRPOS(email, '@'), LENGTH(email))) as masked_email
    FROM customers
""")
```

## 🚀 Production Deployment Best Practices

### Containerization

#### 1. Use Multi-Stage Docker Builds
```dockerfile
# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
CMD ["python", "app.py"]
```

#### 2. Implement Health Checks
```python
# Health check endpoint
def health_check():
    try:
        con = duckdb.connect('database.db')
        con.execute("SELECT 1").fetchone()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Monitoring

#### 1. Track Key Metrics
```python
# Track query performance
query_metrics = {
    'query_time': measure_query_time(),
    'rows_processed': count_rows_processed(),
    'memory_used': get_memory_usage(),
    'cache_hit_rate': calculate_cache_hit_rate()
}
```

#### 2. Implement Alerting
```python
# Alert on performance degradation
if query_metrics['query_time'] > threshold:
    send_alert("Performance degradation detected", query_metrics)
```

## 📈 Scalability Best Practices

### Horizontal Scaling

#### 1. Use Multiple DuckDB Instances
```python
# Distribute queries across instances
instances = ['duckdb-1', 'duckdb-2', 'duckdb-3']

for i, instance in enumerate(instances):
    query = f"""
        SELECT * FROM large_table
        WHERE hash(id) % {len(instances)} = {i}
    """
    execute_on_instance(instance, query)
```

#### 2. Implement Read Replicas
```python
# Use read replicas for query load balancing
primary = 'duckdb-primary'
replicas = ['duckdb-replica-1', 'duckdb-replica-2']

# Write to primary
execute_on_instance(primary, write_query)

# Read from replicas
execute_on_instance(replicas[0], read_query)
```

### Resource Management

#### 1. Implement Connection Pooling
```python
from queue import Queue
import threading

class ConnectionPool:
    def __init__(self, max_size=10):
        self.pool = Queue(max_size)
        for _ in range(max_size):
            self.pool.put(duckdb.connect('database.db'))
    
    def get_connection(self):
        return self.pool.get()
    
    def return_connection(self, conn):
        self.pool.put(conn)
```

#### 2. Use Appropriate Thread Configuration
```python
# Configure based on workload
# OLAP workloads: More threads for parallel processing
con.execute("SET threads=8")

# OLTP workloads: Fewer threads to reduce contention
con.execute("SET threads=2")
```

## 🧪 Testing Best Practices

### Data Testing

#### 1. Implement Data Validation Tests
```python
def test_data_quality():
    # Test for null values
    null_count = con.execute("SELECT COUNT(*) FROM table WHERE column IS NULL").fetchone()[0]
    assert null_count == 0, "Null values found"
    
    # Test for duplicates
    duplicate_count = con.execute("SELECT COUNT(*) - COUNT(DISTINCT id) FROM table").fetchone()[0]
    assert duplicate_count == 0, "Duplicate values found"
```

#### 2. Create Test Data Sets
```python
# Create predictable test data
test_data = [
    (1, 'Test Customer 1', 'test1@example.com'),
    (2, 'Test Customer 2', 'test2@example.com'),
    (3, 'Test Customer 3', 'test3@example.com')
]

con.register('test_data', test_data)
con.execute("CREATE TABLE test_customers AS SELECT * FROM test_data")
```

### Performance Testing

#### 1. Benchmark Critical Queries
```python
import time

def benchmark_query(query, iterations=10):
    times = []
    for _ in range(iterations):
        start = time.time()
        con.execute(query).fetchall()
        times.append(time.time() - start)
    
    return {
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times)
    }
```

## 📝 Documentation Best Practices

### Code Documentation

#### 1. Use Docstrings
```python
def process_customer_data(customer_id):
    """
    Process customer data for lakehouse silver layer.
    
    Args:
        customer_id: Unique customer identifier
        
    Returns:
        DataFrame with processed customer data
        
    Raises:
        ValueError: If customer_id not found
    """
    # Implementation
    pass
```

#### 2. Add Inline Comments
```python
# Load customer data with validation
con.execute("""
    SELECT 
        customer_id,
        first_name,
        -- Validate email format
        CASE 
            WHEN email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$' 
            THEN email 
            ELSE NULL 
        END as validated_email
    FROM customers
""")
```

### Process Documentation

#### 1. Document Data Lineage
```python
# Document data transformations
lineage = {
    'source': 'raw_events',
    'transformations': [
        'email_validation',
        'timestamp_normalization',
        'deduplication'
    ],
    'destination': 'silver_events',
    'schema_changes': [
        'added validated_email column',
        'normalized timestamp format'
    ]
}
```

#### 2. Create Runbooks
```markdown
# Data Quality Issue Resolution Runbook

## Steps
1. Identify affected data
2. Assess impact
3. Determine root cause
4. Implement fix
5. Validate resolution
6. Update monitoring
```

## 🎯 Continuous Improvement

### Regular Reviews

#### 1. Performance Reviews
- Monthly query performance analysis
- Quarterly capacity planning
- Annual architecture review

#### 2. Quality Reviews
- Weekly data quality checks
- Monthly validation rule updates
- Quarterly process improvements

### Monitoring

#### 1. Set Up Dashboards
- Query performance metrics
- Data quality metrics
- Resource utilization
- Error rates

#### 2. Implement Proactive Monitoring
- Query performance degradation alerts
- Data quality threshold breaches
- Resource exhaustion warnings
- Error rate increases

---

**Following these best practices will help you build robust, scalable, and maintainable DuckDB-based lakehouse solutions!**