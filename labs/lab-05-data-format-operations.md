# Lab 5: Data Format Operations

## 🎯 Learning Objectives

- Master Parquet file operations in DuckDB
- Work with Apache Arrow format
- Handle CSV and JSON data efficiently
- Perform data format conversions
- Understand file system operations
- Implement lakehouse data format strategies

## 📋 Prerequisites

- Completed Lab 4: Python Integration
- Working DuckDB environment
- Sample database loaded
- Basic understanding of data formats

## ⏱️ Estimated Time

45-60 minutes

## 🎓 Conceptual Background

Modern data lakehouse architectures rely on efficient data formats. This lab covers:

**Parquet**: Columnar storage format optimized for analytical workloads
**Apache Arrow**: In-memory columnar format for zero-copy data sharing
**CSV/JSON**: Traditional formats for data interchange
**Format Conversion**: Transforming between different formats
**File System Operations**: Reading and writing files efficiently
**Lakehouse Format Strategy**: Choosing the right format for each layer

## 🚀 Step-by-Step Instructions

### Step 1: Parquet Operations

Master Parquet file operations, the cornerstone of lakehouse architectures.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Read Parquet files
print("Reading Parquet files...")

# Read from local Parquet file
df_customers = con.execute("SELECT * FROM 'data/sample/customers.parquet'").df()
print(f"Customers from Parquet: {len(df_customers)} rows")

# Read specific columns (column pruning)
df_subset = con.execute("""
    SELECT customer_id, first_name, segment 
    FROM 'data/sample/customers.parquet'
""").df()
print(f"Subset from Parquet: {df_subset.shape}")

# Push-down predicates
df_filtered = con.execute("""
    SELECT * FROM 'data/sample/customers.parquet'
    WHERE segment = 'Premium'
""").df()
print(f"Filtered from Parquet: {len(df_filtered)} rows")

# Write to Parquet
print("Writing to Parquet...")

# Export table to Parquet
con.execute("""
    COPY sample_customers TO 'data/output/customers_export.parquet' 
    (FORMAT PARQUET, COMPRESSION 'snappy')
""")
print("Exported customers to Parquet")

# Export query results to Parquet
con.execute("""
    COPY (
        SELECT segment, COUNT(*) as count, AVG(loyalty_points) as avg_points
        FROM sample_customers
        GROUP BY segment
    ) TO 'data/output/segment_summary.parquet' 
    (FORMAT PARQUET)
""")
print("Exported segment summary to Parquet")

# Verify Parquet export
df_export = con.execute("SELECT * FROM 'data/output/customers_export.parquet' LIMIT 5").df()
print("Parquet export verification:")
print(df_export)
```

### Step 2: Apache Arrow Integration

Work with Apache Arrow for zero-copy data operations.

```python
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

con = duckdb.connect('data/duckdb_practice.db')

# Convert DuckDB results to Arrow
print("Converting to Arrow format...")

# Query to Arrow table
arrow_table = con.execute("SELECT * FROM sample_customers LIMIT 100").arrow()
print(f"Arrow table schema: {arrow_table.schema}")
print(f"Arrow table shape: {arrow_table.num_rows} rows, {arrow_table.num_columns} columns")

# Arrow to DuckDB (zero-copy)
con.register('customers_arrow', arrow_table)
result = con.execute("SELECT COUNT(*) FROM customers_arrow").fetchone()
print(f"Registered Arrow table: {result[0]} rows")

# Arrow file operations
print("Arrow file operations...")

# Write to Arrow file
con.execute("""
    COPY sample_products TO 'data/output/products.arrow' 
    (FORMAT ARROW)
""")
print("Exported products to Arrow format")

# Read from Arrow file
df_arrow = con.execute("SELECT * FROM 'data/output/products.arrow'").df()
print(f"Products from Arrow: {len(df_arrow)} rows")

# Arrow memory mapping (zero-copy)
# This is efficient for large datasets
arrow_memory = con.execute("""
    SELECT * FROM 'data/output/products.arrow'
""").arrow()
print(f"Arrow memory-mapped table: {arrow_memory.num_rows} rows")

# Convert between Arrow and Parquet
print("Arrow-Parquet conversion...")

# Arrow to Parquet
pq.write_table(arrow_memory, 'data/output/products_from_arrow.parquet')
print("Converted Arrow to Parquet")

# Parquet to Arrow
arrow_from_parquet = pq.read_table('data/output/products_from_arrow.parquet')
print(f"Parquet to Arrow: {arrow_from_parquet.num_rows} rows")
```

### Step 3: CSV Operations

Handle CSV files efficiently with DuckDB.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Read CSV files
print("Reading CSV files...")

# Read from CSV
df_csv = con.execute("""
    SELECT * FROM 'data/sample/customers.csv' 
    LIMIT 10
""").df()
print(f"Customers from CSV: {df_csv.shape}")

# CSV with automatic schema detection
df_csv_auto = con.execute("""
    SELECT * FROM read_csv_auto('data/sample/customers.csv')
    LIMIT 5
""").df()
print("CSV with auto-detection:")
print(df_csv_auto)

# CSV with custom options
df_csv_custom = con.execute("""
    SELECT * FROM read_csv(
        'data/sample/customers.csv',
        header = true,
        delim = ',',
        quote = '"',
        escape = '"',
        nullstr = 'NULL'
    )
    LIMIT 5
""").df()
print("CSV with custom options:")
print(df_csv_custom)

# Write to CSV
print("Writing to CSV...")

# Export to CSV
con.execute("""
    COPY (
        SELECT customer_id, first_name, segment, loyalty_points
        FROM sample_customers
        WHERE segment = 'Premium'
    ) TO 'data/output/premium_customers.csv' 
    (HEADER, DELIMITER ',')
""")
print("Exported premium customers to CSV")

# CSV with custom formatting
con.execute("""
    COPY (
        SELECT segment, COUNT(*) as customer_count
        FROM sample_customers
        GROUP BY segment
    ) TO 'data/output/segment_counts.csv' 
    (HEADER, DELIMITER ',', QUOTE '"')
""")
print("Exported segment counts to CSV")

# Verify CSV export
csv_verify = con.execute("""
    SELECT * FROM 'data/output/premium_customers.csv' 
    LIMIT 5
""").df()
print("CSV export verification:")
print(csv_verify)
```

### Step 4: JSON Operations

Work with JSON data for flexible data interchange.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Generate sample JSON data
print("Generating JSON data...")

con.execute("""
    COPY (
        SELECT 
            customer_id,
            first_name,
            last_name,
            email,
            segment,
            loyalty_points,
            is_active
        FROM sample_customers
        LIMIT 10
    ) TO 'data/output/customers.json' 
    (ARRAY false)
""")
print("Exported customers to JSON")

# Read JSON files
print("Reading JSON files...")

# Read from JSON
df_json = con.execute("""
    SELECT * FROM 'data/output/customers.json'
""").df()
print(f"Customers from JSON: {df_json.shape}")

# JSON with auto-detection
df_json_auto = con.execute("""
    SELECT * FROM read_json_auto('data/output/customers.json')
    LIMIT 5
""").df()
print("JSON with auto-detection:")
print(df_json_auto)

# Query nested JSON structures
# Create nested JSON example
con.execute("""
    COPY (
        SELECT 
            customer_id,
            first_name,
            {
                'segment': segment,
                'loyalty_points': loyalty_points,
                'is_active': is_active,
                'registration_date': registration_date
            } as customer_info
        FROM sample_customers
        LIMIT 5
    ) TO 'data/output/customers_nested.json' 
    (ARRAY false)
""")
print("Exported nested JSON")

# Query nested JSON
df_nested = con.execute("""
    SELECT 
        customer_id,
        customer_info->'segment' as segment,
        customer_info->'loyalty_points' as loyalty_points
    FROM 'data/output/customers_nested.json'
""").df()
print("Nested JSON query:")
print(df_nested)
```

### Step 5: Data Format Conversion

Convert between different data formats efficiently.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Parquet to CSV conversion
print("Parquet to CSV conversion...")
con.execute("""
    COPY (
        SELECT * FROM 'data/sample/customers.parquet' LIMIT 100
    ) TO 'data/output/customers_parquet_to_csv.csv' 
    (HEADER, DELIMITER ',')
""")
print("Converted Parquet to CSV")

# CSV to Parquet conversion
print("CSV to Parquet conversion...")
con.execute("""
    COPY (
        SELECT * FROM 'data/sample/customers.csv' LIMIT 100
    ) TO 'data/output/customers_csv_to_parquet.parquet' 
    (FORMAT PARQUET)
""")
print("Converted CSV to Parquet")

# Parquet to Arrow conversion
print("Parquet to Arrow conversion...")
con.execute("""
    COPY (
        SELECT * FROM 'data/sample/customers.parquet' LIMIT 100
    ) TO 'data/output/customers_parquet_to_arrow.arrow' 
    (FORMAT ARROW)
""")
print("Converted Parquet to Arrow")

# Format comparison
print("Format size comparison...")

import os

parquet_size = os.path.getsize('data/sample/customers.parquet')
csv_size = os.path.getsize('data/sample/customers.csv')

print(f"Parquet file size: {parquet_size:,} bytes")
print(f"CSV file size: {csv_size:,} bytes")
print(f"Compression ratio: {csv_size / parquet_size:.2f}x")

# Performance comparison
import time

# Parquet read time
start = time.time()
con.execute("SELECT COUNT(*) FROM 'data/sample/customers.parquet'").fetchone()
parquet_time = time.time() - start

# CSV read time
start = time.time()
con.execute("SELECT COUNT(*) FROM 'data/sample/customers.csv'").fetchone()
csv_time = time.time() - start

print(f"Parquet read time: {parquet_time:.4f} seconds")
print(f"CSV read time: {csv_time:.4f} seconds")
print(f"Performance improvement: {csv_time / parquet_time:.2f}x")
```

### Step 6: Lakehouse Format Strategy

Implement data format strategies for lakehouse architecture.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Lakehouse format strategy
print("Lakehouse format strategy...")

# Bronze layer: Raw data in Parquet (append-only, immutable)
print("Bronze layer strategy...")

con.execute("""
    COPY (
        SELECT * FROM sample_orders
        WHERE order_date >= '2022-01-01'
    ) TO 'data/lakehouse/bronze/orders_raw.parquet' 
    (FORMAT PARQUET, COMPRESSION 'snappy')
""")
print("Bronze layer: Raw orders in Parquet")

# Silver layer: Cleaned data in Parquet (partitioned)
print("Silver layer strategy...")

con.execute("""
    COPY (
        SELECT 
            order_id,
            customer_id,
            product_id,
            order_date,
            quantity,
            unit_price,
            CASE 
                WHEN total_amount <= 0 OR total_amount IS NULL THEN NULL
                ELSE total_amount
            END as total_amount,
            CASE 
                WHEN status NOT IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled') THEN 'unknown'
                ELSE status
            END as status,
            payment_method,
            CURRENT_TIMESTAMP as processed_timestamp
        FROM sample_orders
        WHERE order_date >= '2022-01-01'
    ) TO 'data/lakehouse/silver/orders_clean.parquet' 
    (FORMAT PARQUET, COMPRESSION 'zstd')
""")
print("Silver layer: Cleaned orders in Parquet with ZSTD compression")

# Gold layer: Aggregated metrics in Parquet (optimized for queries)
print("Gold layer strategy...")

con.execute("""
    COPY (
        SELECT 
            DATE_TRUNC('month', order_date) as month,
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers,
            SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders
        FROM (
            SELECT 
                order_id,
                customer_id,
                order_date,
                total_amount,
                status
            FROM sample_orders
            WHERE order_date >= '2022-01-01'
        ) silver_orders
        WHERE total_amount IS NOT NULL
        GROUP BY month
        ORDER BY month
    ) TO 'data/lakehouse/gold/monthly_metrics.parquet' 
    (FORMAT PARQUET, COMPRESSION 'snappy', ROW_GROUP_SIZE 100000)
""")
print("Gold layer: Monthly metrics in optimized Parquet")

# Format strategy analysis
print("Format strategy analysis...")

bronze_size = os.path.getsize('data/lakehouse/bronze/orders_raw.parquet')
silver_size = os.path.getsize('data/lakehouse/silver/orders_clean.parquet')
gold_size = os.path.getsize('data/lakehouse/gold/monthly_metrics.parquet')

print(f"Bronze layer size: {bronze_size:,} bytes")
print(f"Silver layer size: {silver_size:,} bytes")
print(f"Gold layer size: {gold_size:,} bytes")
print(f"Silver compression ratio: {bronze_size / silver_size:.2f}x")
print(f"Gold compression ratio: {silver_size / gold_size:.2f}x")

# Query performance by layer
import time

layers = [
    ('Bronze', "SELECT COUNT(*) FROM 'data/lakehouse/bronze/orders_raw.parquet'"),
    ('Silver', "SELECT COUNT(*) FROM 'data/lakehouse/silver/orders_clean.parquet'"),
    ('Gold', "SELECT COUNT(*) FROM 'data/lakehouse/gold/monthly_metrics.parquet'")
]

for layer_name, query in layers:
    start = time.time()
    con.execute(query).fetchone()
    query_time = time.time() - start
    print(f"{layer_name} query time: {query_time:.4f} seconds")
```

## 💻 Hands-On Exercises

### Exercise 1: Build Format Conversion Pipeline

Create a comprehensive format conversion pipeline:

```python
# Your code here
# Convert between Parquet, CSV, JSON, Arrow
# Handle format-specific options
# Optimize for different use cases
# Validate conversions
# Log conversion metrics
```

### Exercise 2: Implement Partitioning Strategy

Implement data partitioning for lakehouse efficiency:

```python
# Your code here
# Design partitioning strategy
# Implement date-based partitioning
# Implement category-based partitioning
# Query partitioned data efficiently
# Manage partition maintenance
```

### Exercise 3: Format Performance Analysis

Analyze performance characteristics of different formats:

```python
# Your code here
# Benchmark read/write performance
# Compare compression ratios
# Analyze query performance
# Test with different data sizes
# Generate performance reports
```

### Exercise 4: Data Format Validation

Implement data format validation framework:

```python
# Your code here
# Validate file schemas
# Check data integrity
# Validate format compliance
# Handle format errors
# Create validation reports
```

### Exercise 5: Lakehouse Format Optimization

Optimize data formats for lakehouse architecture:

```python
# Your code here
# Optimize compression settings
# Configure row group sizes
# Implement column pruning
# Design format lifecycle
# Monitor format performance
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Master Parquet file operations
2. ✅ Work with Apache Arrow efficiently
3. ✅ Handle CSV and JSON data
4. ✅ Perform format conversions
5. ✅ Understand lakehouse format strategies
6. ✅ Optimize data formats for performance

## 🔍 Verification

Test your data format skills:

```python
import duckdb
import os

con = duckdb.connect('data/duckdb_practice.db')

# Test Parquet operations
parquet_test = con.execute("SELECT COUNT(*) FROM 'data/sample/customers.parquet'").fetchone()
print(f"Parquet test: {parquet_test[0]} rows")

# Test format conversion
conversion_test = os.path.exists('data/output/customers_parquet_to_csv.csv')
print(f"Format conversion test: {conversion_test}")

# Test lakehouse layers
lakehouse_test = all([
    os.path.exists('data/lakehouse/bronze/orders_raw.parquet'),
    os.path.exists('data/lakehouse/silver/orders_clean.parquet'),
    os.path.exists('data/lakehouse/gold/monthly_metrics.parquet')
])
print(f"Lakehouse layers test: {lakehouse_test}")

print("✅ Data format operations test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: Parquet read errors

**Solution**: Check file integrity and compatibility:
```python
# Validate Parquet file
con.execute("SELECT COUNT(*) FROM 'file.parquet'").fetchone()

# Try different readers
con.execute("SELECT * FROM read_parquet('file.parquet', union_by_name=True)")
```

### Issue: Memory errors with large files

**Solution**: Process in chunks or use memory mapping:
```python
# Process in chunks
for chunk in con.execute("SELECT * FROM large_file.parquet").fetchmany(1000):
    # Process chunk
    pass

# Use memory mapping
con.execute("SET enable_object_cache=true")
```

### Issue: Format conversion failures

**Solution**: Handle data type mismatches explicitly:
```python
# Explicit type casting
con.execute("""
    COPY (
        SELECT CAST(column AS VARCHAR) FROM table
    ) TO 'output.csv' (HEADER)
""")
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 6**: Performance Optimization
2. **Study format best practices**: Deep dive into Parquet optimization
3. **Implement partitioning**: Apply to real datasets
4. **Build format monitoring**: Track format performance

---

**You now have comprehensive data format skills for building efficient lakehouse architectures!**