# Lab 1A: Introduction to DuckDB

## 🎯 Learning Objectives

- Understand what DuckDB is and its core characteristics
- Learn why DuckDB matters in modern data analytics
- Identify when to use DuckDB vs. other databases
- Understand DuckDB's place in the data processing ecosystem
- Explore DuckDB use cases and real-world applications
- Understand the data processing flow with DuckDB

## 📋 Prerequisites

- Basic understanding of SQL concepts
- Python 3.8+ installed
- DuckDB Python package installed
- Completed Lab 0: Sample Database Setup

## ⏱️ Estimated Time

45-60 minutes

## 🎓 Conceptual Background

### What is DuckDB?

DuckDB is an in-memory analytical database system designed for fast query execution on structured data. Key characteristics:

- **In-Memory OLAP**: Optimized for analytical workloads with columnar storage
- **Embedded Database**: Runs in-process, no separate server needed
- **SQL Compliant**: Supports standard SQL with extensions
- **Zero Configuration**: Works out of the box with minimal setup
- **Cross-Platform**: Runs on Linux, macOS, Windows, and in browsers

### Why Should You Care About DuckDB?

DuckDB addresses several pain points in modern data analytics:

1. **Performance**: Vectorized execution engine for fast queries
2. **Simplicity**: No server setup, embedded deployment
3. **Compatibility**: Works with Python, R, Java, and more
4. **Portability**: Single-file databases, easy to move
5. **Cost-Effective**: No infrastructure costs for local development
6. **Integration**: Seamless integration with pandas, Arrow, and other tools

### When Should You Use DuckDB?

**Ideal Use Cases:**
- Local data analysis and exploration
- Embedded analytics in applications
- Data science and machine learning workflows
- ETL and data transformation pipelines
- Prototyping and testing data solutions
- Educational and learning environments

**Data Characteristics:**
- Structured/semi-structured data (CSV, Parquet, JSON)
- Medium-sized datasets (up to terabytes)
- Read-heavy analytical workloads
- Complex aggregations and joins

### When Should You NOT Use DuckDB?

**Not Ideal For:**
- High-concurrency transactional workloads
- Real-time streaming data processing
- Multi-user collaborative environments
- Large-scale distributed data processing
- Complex transaction management requirements

**Consider Alternatives For:**
- PostgreSQL for transactional workloads
- Apache Spark for distributed processing
- SQLite for embedded transactional use
- ClickHouse for large-scale analytics

### DuckDB Use Cases

1. **Data Science & ML**
   - Feature engineering and data preprocessing
   - Model training data preparation
   - Experiment result analysis

2. **Business Intelligence**
   - Local dashboard development
   - Report generation
   - Ad-hoc data exploration

3. **Data Engineering**
   - ETL pipeline development
   - Data validation and testing
   - Format conversion (CSV to Parquet)

4. **Application Development**
   - Embedded analytics features
   - Local data caching
   - Offline-first applications

### Where Does DuckDB Fit In?

DuckDB fits into the modern data ecosystem in several ways:

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Ecosystem                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Data Sources          Processing           Output         │
│  ┌──────────┐        ┌──────────┐       ┌──────────┐      │
│  │   CSV    │───────▶│ DuckDB   │───────▶│ Pandas   │      │
│  │  Parquet │        │          │       │  Arrow   │      │
│  │   JSON   │        │          │       │ Reports  │      │
│  │  SQLite  │        │          │       │   Apps   │      │
│  └──────────┘        └──────────┘       └──────────┘      │
│                              ↓                              │
│                      Integration Layer                     │
│                      - Python API                          │
│                      - SQL Shell                           │
│                      - CLI Tools                            │
└─────────────────────────────────────────────────────────────┘
```

### Data Processing Flow with DuckDB

#### Step 1: Data Formats and Sources

DuckDB supports multiple data formats and sources:

```python
import duckdb

# CSV files
con.execute("SELECT * FROM 'data.csv'")

# Parquet files (columnar, efficient)
con.execute("SELECT * FROM 'data.parquet'")

# JSON files
con.execute("SELECT * FROM 'data.json'")

# SQLite databases
con.execute("SELECT * FROM sqlite_scan('database.db', 'table_name')")

# HTTP endpoints (with extensions)
con.execute("SELECT * FROM 'https://example.com/data.parquet'")
```

#### Step 2: Data Structures

DuckDB provides flexible data structures:

```python
# Tables (persistent)
con.execute("CREATE TABLE customers AS SELECT * FROM 'customers.csv'")

# Views (virtual tables)
con.execute("CREATE VIEW premium_customers AS SELECT * FROM customers WHERE segment = 'Premium'")

# In-memory queries (ephemeral)
con.execute("SELECT * FROM 'data.parquet' WHERE date > '2023-01-01'")

# Temporary tables
con.execute("CREATE TEMP TABLE temp_data AS SELECT * FROM large_data LIMIT 1000")
```

#### Step 3: Developing the SQL

DuckDB extends standard SQL with powerful features:

```python
# Standard SQL
con.execute("""
    SELECT customer_id, SUM(amount) as total
    FROM orders
    GROUP BY customer_id
""")

# DuckDB extensions
con.execute("""
    SELECT customer_id, SUM(amount) as total
    FROM orders
    GROUP BY ALL
""")

# Window functions
con.execute("""
    SELECT 
        customer_id,
        amount,
        SUM(amount) OVER (PARTITION BY customer_id ORDER BY date) as running_total
    FROM orders
""")
```

#### Step 4: Using or Processing the Results

Multiple output options:

```python
# Fetch as Python list
results = con.execute("SELECT * FROM customers").fetchall()

# Fetch as pandas DataFrame
df = con.execute("SELECT * FROM customers").df()

# Fetch as Arrow table
import pyarrow as pa
table = con.execute("SELECT * FROM customers").arrow()

# Export to different formats
con.execute("COPY customers TO 'output.csv' (FORMAT CSV)")
con.execute("COPY customers TO 'output.parquet' (FORMAT PARQUET)")
```

## 🚀 Step-by-Step Instructions

### Step 1: Explore DuckDB Characteristics

Let's explore DuckDB's core characteristics:

```python
import duckdb

# Check DuckDB version
print(f"DuckDB version: {duckdb.__version__}")

# Create an in-memory database
con = duckdb.connect(':memory:')

# Check database configuration
config = con.execute("SELECT * FROM duckdb_settings() WHERE name LIKE '%memory%'").fetchall()
print("Memory-related settings:")
for setting in config:
    print(f"  {setting[0]}: {setting[1]}")
```

### Step 2: Compare DuckDB Performance

Compare DuckDB with other approaches for simple analytics:

```python
import duckdb
import pandas as pd
import time

# Create sample data
con = duckdb.connect(':memory:')
con.execute("""
    CREATE TABLE test_data AS 
    SELECT * FROM range(1000000) 
    CROSS JOIN (SELECT random() as value FROM range(10))
""")

# DuckDB query
start = time.time()
duckdb_result = con.execute("SELECT AVG(value) FROM test_data").fetchone()
duckdb_time = time.time() - start

# Convert to pandas and query
start = time.time()
df = con.execute("SELECT * FROM test_data").df()
pandas_result = df['value'].mean()
pandas_time = time.time() - start

print(f"DuckDB time: {duckdb_time:.4f}s, Result: {duckdb_result[0]}")
print(f"Pandas time: {pandas_time:.4f}s, Result: {pandas_result}")
```

### Step 3: Practice Data Format Handling

Explore different data format capabilities:

```python
import duckdb

con = duckdb.connect(':memory:')

# Create sample data in different formats
con.execute("""
    CREATE TABLE sample_data AS
    SELECT 
        id,
        'Product ' || id as name,
        random() * 100 as price,
        (random() * 1000)::int as quantity
    FROM range(100)
""")

# Export to different formats
con.execute("COPY sample_data TO 'data/sample.csv' (FORMAT CSV, HEADER)")
con.execute("COPY sample_data TO 'data/sample.parquet' (FORMAT PARQUET)")
con.execute("COPY sample_data TO 'data/sample.json' (FORMAT JSON)")

# Read from different formats
csv_data = con.execute("SELECT COUNT(*) FROM 'data/sample.csv'").fetchone()
parquet_data = con.execute("SELECT COUNT(*) FROM 'data/sample.parquet'").fetchone()
json_data = con.execute("SELECT COUNT(*) FROM 'data/sample.json'").fetchone()

print(f"CSV records: {csv_data[0]}")
print(f"Parquet records: {parquet_data[0]}")
print(f"JSON records: {json_data[0]}")
```

### Step 4: Explore DuckDB's SQL Extensions

Practice DuckDB-specific SQL features:

```python
import duckdb

con = duckdb.connect(':memory:')
con.execute("""
    CREATE TABLE sales AS
    SELECT 
        (random() * 100)::int as product_id,
        (random() * 50 + 1)::int as quantity,
        random() * 100 as price,
        '2023-01-01'::date + (random() * 365)::int as date
    FROM range(1000)
""")

# GROUP BY ALL (DuckDB extension)
result = con.execute("""
    SELECT product_id, AVG(price), SUM(quantity)
    FROM sales
    GROUP BY ALL
""").fetchall()
print("GROUP BY ALL results:", result[:5])

# Sampling
sample = con.execute("""
    SELECT * FROM sales
    USING SAMPLE 10%
""").fetchdf()
print(f"Sampled {len(sample)} rows from 1000")

# Optional parameters in functions
result = con.execute("""
    SELECT 
        product_id,
        quantile(price, 0.5) as median,
        quantile(price, 0.5, 'nearest') as median_nearest
    FROM sales
    GROUP BY product_id
""").fetchdf()
print("Quantile with options:", result.head())
```

### Step 5: Understand Data Processing Flow

Practice the complete data processing flow:

```python
import duckdb

con = duckdb.connect(':memory:')

# Step 1: Data ingestion from CSV
con.execute("""
    CREATE TABLE raw_customers AS
    SELECT * FROM read_csv_auto('data/sample/customers.csv')
""")

# Step 2: Data transformation
con.execute("""
    CREATE TABLE processed_customers AS
    SELECT 
        customer_id,
        UPPER(first_name) as first_name,
        UPPER(last_name) as last_name,
        segment,
        registration_date,
        CASE 
            WHEN loyalty_points > 5000 THEN 'Gold'
            WHEN loyalty_points > 2000 THEN 'Silver'
            ELSE 'Bronze'
        END as loyalty_tier
    FROM raw_customers
""")

# Step 3: Data aggregation
con.execute("""
    CREATE TABLE customer_summary AS
    SELECT 
        segment,
        loyalty_tier,
        COUNT(*) as customer_count,
        AVG(loyalty_points) as avg_loyalty
    FROM processed_customers
    GROUP BY segment, loyalty_tier
""")

# Step 4: Data export
con.execute("COPY customer_summary TO 'data/customer_summary.csv' (FORMAT CSV, HEADER)")

# Step 5: Results processing
summary = con.execute("SELECT * FROM customer_summary").df()
print(summary)
```

## 💻 Hands-On Exercises

### Exercise 1: DuckDB Use Case Analysis

Identify appropriate use cases for DuckDB:

```python
# For each scenario, determine if DuckDB is a good fit and why

scenarios = [
    "Real-time inventory management for e-commerce",
    "Local data analysis for a data science project",
    "Multi-user business intelligence dashboard",
    "ETL pipeline for data warehouse",
    "Embedded analytics in a desktop application"
]

for scenario in scenarios:
    # Your analysis here
    print(f"Scenario: {scenario}")
    print("DuckDB fit: [Good/Marginal/Poor]")
    print("Reason: [Your reasoning]")
    print()
```

### Exercise 2: Data Format Comparison

Compare different data formats:

```python
import duckdb
import time
import os

con = duckdb.connect(':memory:')

# Create test data
con.execute("""
    CREATE TABLE test_data AS
    SELECT 
        id,
        'Name ' || id as name,
        random() * 1000 as value,
        '2023-01-01'::date + (random() * 365)::int as date
    FROM range(100000)
""")

# Test different formats
formats = ['csv', 'parquet', 'json']
for format in formats:
    # Export
    start = time.time()
    con.execute(f"COPY test_data TO 'data/test.{format}' (FORMAT {format.upper()})")
    export_time = time.time() - start
    
    # Import
    start = time.time()
    con.execute(f"SELECT COUNT(*) FROM 'data/test.{format}'").fetchone()
    import_time = time.time() - start
    
    # File size
    file_size = os.path.getsize(f'data/test.{format}') / 1024  # KB
    
    print(f"{format.upper()}: Export {export_time:.4f}s, Import {import_time:.4f}s, Size {file_size:.2f}KB")
```

### Exercise 3: SQL Extension Practice

Practice DuckDB-specific SQL features:

```python
import duckdb

con = duckdb.connect(':memory:')
con.execute("""
    CREATE TABLE orders AS
    SELECT 
        (random() * 100)::int as customer_id,
        (random() * 50)::int as product_id,
        random() * 500 as amount,
        ['pending', 'processing', 'shipped', 'delivered'][((random() * 4)::int)] as status,
        '2023-01-01'::date + (random() * 365)::int as order_date
    FROM range(10000)
""")

# Practice GROUP BY ALL
# Your code here

# Practice sampling
# Your code here

# Practice QUALIFY clause
# Your code here

# Practice FILTER clause
# Your code here
```

### Exercise 4: Integration Flow

Create a complete data processing pipeline:

```python
import duckdb

con = duckdb.connect(':memory:')

# Create a pipeline that:
# 1. Reads data from multiple sources
# 2. Transforms and cleans the data
# 3. Performs aggregations
# 4. Exports results in multiple formats

# Your implementation here
```

### Exercise 5: Performance Comparison

Compare DuckDB with other tools for specific tasks:

```python
# Choose a specific analytical task and compare DuckDB with another tool
# Examples: pandas, SQLite, pure Python

import duckdb
import pandas as pd
import time

# Your performance comparison code here
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Understand DuckDB's core characteristics and advantages
2. ✅ Know when to use DuckDB vs. other databases
3. ✅ Be familiar with DuckDB's place in the data ecosystem
4. ✅ Understand the complete data processing flow with DuckDB
5. ✅ Have practiced DuckDB-specific SQL extensions
6. ✅ Be able to evaluate DuckDB for different use cases

## 🔍 Verification

Verify your understanding with this comprehensive check:

```python
import duckdb

print("=== DuckDB Knowledge Verification ===")

# Test 1: Data format handling
con = duckdb.connect(':memory:')
con.execute("CREATE TABLE test AS SELECT * FROM range(100)")
con.execute("COPY test TO 'data/test.csv' (FORMAT CSV)")
csv_count = con.execute("SELECT COUNT(*) FROM 'data/test.csv'").fetchone()[0]
print(f"✓ Data format handling: {csv_count} == 100")

# Test 2: SQL extensions
con.execute("CREATE TABLE sales AS SELECT * FROM range(1000)")
group_result = con.execute("SELECT COUNT(*) FROM sales GROUP BY ALL").fetchall()
print(f"✓ GROUP BY ALL: {len(group_result)} groups")

# Test 3: Performance
import time
start = time.time()
con.execute("SELECT AVG(column0) FROM sales").fetchone()
query_time = time.time() - start
print(f"✓ Performance: Query completed in {query_time:.4f}s")

print("=== All Verification Tests Passed ===")
```

## 🆘 Troubleshooting

### Issue: DuckDB performance seems slow

**Solution**: Check memory configuration and data format:
```python
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=8")
```

### Issue: Data format reading fails

**Solution**: Use `read_csv_auto` for automatic detection:
```python
con.execute("SELECT * FROM read_csv_auto('data.csv')")
```

### Issue: Memory errors with large datasets

**Solution**: Use streaming or process in batches:
```python
con.execute("SET enable_progress_bar=true")
# Process data in chunks
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 2**: Getting Started with DuckDB
2. **Read DuckDB documentation**: https://duckdb.org/docs/
3. **Practice more**: Explore different data formats and SQL extensions

---

**You now have a solid understanding of DuckDB and its place in modern data analytics!**