# DuckDB Fundamentals

This guide covers the fundamental concepts of DuckDB that you need to understand before diving into the labs.

## 🎯 What is DuckDB?

DuckDB is an in-memory SQL OLAP (Online Analytical Processing) database management system. It's designed for analytical query processing and is optimized for speed and efficiency.

### Key Characteristics

- **Embedded Database**: Runs as an embedded library, no separate server process
- **Columnar Storage**: Uses columnar storage for analytical efficiency
- **Zero-Copy Integration**: Seamless integration with Arrow and pandas
- **SQL Compliant**: Supports standard SQL with analytical extensions
- **Vectorized Execution**: Processes data in batches for performance
- **Cross-Platform**: Works on Linux, macOS, and Windows

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│         Client Interface               │
│  (Python, SQL Shell, JDBC/ODBC)        │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         Query Parser & Optimizer       │
│  (SQL parsing, query planning)         │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         Execution Engine                │
│  (Vectorized execution, parallelism)   │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         Storage Engine                 │
│  (Columnar storage, compression)       │
└─────────────────────────────────────────┘
```

### Storage Model

DuckDB uses columnar storage, which means:

- **Column-Oriented**: Data is stored by column, not by row
- **Compression**: Better compression ratios for similar data
- **Analytical Performance**: Efficient for aggregations and analytics
- **Selective Loading**: Only read needed columns

## 🗄️ Database Operations

### Connection Modes

#### In-Memory Database
```python
import duckdb
con = duckdb.connect(':memory:')
```
- Fastest performance
- Data lost when connection closes
- Good for temporary data and testing

#### Persistent Database
```python
con = duckdb.connect('my_database.db')
```
- Data persisted to disk
- Survives connection closure
- Good for long-term storage

#### Read-Only Connection
```python
con = duckdb.connect('my_database.db', read_only=True)
```
- Prevents accidental modifications
- Good for reporting and analysis

### Basic Operations

#### Creating Tables
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    created_at TIMESTAMP
);
```

#### Inserting Data
```sql
INSERT INTO customers VALUES 
(1, 'John Doe', 'john@example.com', '2023-01-01 10:00:00'),
(2, 'Jane Smith', 'jane@example.com', '2023-01-02 11:00:00');
```

#### Querying Data
```sql
SELECT * FROM customers WHERE name LIKE 'J%';
SELECT COUNT(*) FROM customers;
SELECT name, email FROM customers ORDER BY created_at DESC;
```

#### Updating Data
```sql
UPDATE customers SET email = 'newemail@example.com' WHERE id = 1;
```

#### Deleting Data
```sql
DELETE FROM customers WHERE id = 2;
```

## 🔢 Data Types

### Numeric Types

- **INTEGER**: 32-bit integer
- **BIGINT**: 64-bit integer
- **FLOAT**: 32-bit floating point
- **DOUBLE**: 64-bit floating point
- **DECIMAL(p,s)**: Fixed-point decimal

### String Types

- **VARCHAR**: Variable-length string
- **TEXT**: Long text (alias for VARCHAR)

### Date/Time Types

- **DATE**: Date (year, month, day)
- **TIME**: Time (hour, minute, second)
- **TIMESTAMP**: Date and time
- **INTERVAL**: Time duration

### Boolean Type

- **BOOLEAN**: True/False values

### Special Types

- **JSON**: JSON data
- **UUID**: Universally unique identifier
- **BLOB**: Binary large object

## 🔍 Query Features

### SQL Functions

#### Aggregate Functions
```sql
SELECT COUNT(*), SUM(amount), AVG(amount), 
       MIN(amount), MAX(amount) FROM orders;
```

#### Window Functions
```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

#### Conditional Expressions
```sql
SELECT name,
       CASE 
         WHEN salary > 100000 THEN 'High'
         WHEN salary > 50000 THEN 'Medium'
         ELSE 'Low'
       END as salary_level
FROM employees;
```

### Join Types

```sql
-- Inner Join
SELECT * FROM customers c JOIN orders o ON c.id = o.customer_id;

-- Left Join
SELECT * FROM customers c LEFT JOIN orders o ON c.id = o.customer_id;

-- Right Join
SELECT * FROM customers c RIGHT JOIN orders o ON c.id = o.customer_id;

-- Full Outer Join
SELECT * FROM customers c FULL OUTER JOIN orders o ON c.id = o.customer_id;
```

## ⚡ Performance Features

### Vectorized Execution

DuckDB processes data in batches (vectors) rather than row by row:

- **Cache Efficiency**: Better CPU cache utilization
- **SIMD Optimization**: Uses CPU vector instructions
- **Parallel Processing**: Multi-threaded execution

### Query Optimization

DuckDB includes a cost-based optimizer:

- **Query Planning**: Chooses efficient execution plans
- **Predicate Pushdown**: Filters data early in the pipeline
- **Column Pruning**: Only reads needed columns

### Memory Management

```python
# Set memory limit
con.execute("SET memory_limit='4GB'")

# Set thread count
con.execute("SET threads=4")

# Enable memory profiling
con.execute("SET enable_memory_profiling=true")
```

## 🔌 Extensions

DuckDB supports extensions for additional functionality:

### HTTP Filesystem
```python
con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

# Query remote data
con.execute("SELECT * FROM 'https://example.com/data.parquet'")
```

### Parquet
```python
con.execute("INSTALL parquet")
con.execute("LOAD parquet")

# Advanced Parquet support
con.execute("COPY table TO 'output.parquet' (FORMAT PARQUET)")
```

### JSON
```python
con.execute("INSTALL json")
con.execute("LOAD json")

# Query JSON data
con.execute("SELECT * FROM 'data.json'")
```

### Spatial
```python
con.execute("INSTALL spatial")
con.execute("LOAD spatial")

# Geospatial operations
con.execute("SELECT ST_AsText(ST_Point(1, 2))")
```

## 🐍 Python Integration

### Basic Usage
```python
import duckdb

# Connect
con = duckdb.connect('database.db')

# Execute query
result = con.execute("SELECT * FROM table").fetchall()

# Execute and fetch as DataFrame
df = con.execute("SELECT * FROM table").df()

# Close
con.close()
```

### Pandas Integration
```python
import pandas as pd
import duckdb

# Create DataFrame
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# Query with DuckDB
result = duckdb.query("SELECT a, b FROM df WHERE a > 1").to_df()

# Register DataFrame
con = duckdb.connect()
con.register('my_df', df)
result = con.execute("SELECT * FROM my_df").fetchall()
```

### Arrow Integration
```python
import pyarrow as pa
import duckdb

# Create Arrow table
table = pa.table({'a': [1, 2, 3], 'b': [4, 5, 6]})

# Query with DuckDB
result = duckdb.query("SELECT * FROM table").to_arrow_table()
```

## 📊 Data Formats

### Parquet
```python
# Read Parquet
con.execute("SELECT * FROM 'data.parquet'")

# Write Parquet
con.execute("COPY table TO 'output.parquet' (FORMAT PARQUET)")
```

### CSV
```python
# Read CSV
con.execute("SELECT * FROM 'data.csv'")

# Write CSV
con.execute("COPY table TO 'output.csv' (HEADER, DELIMITER ',')")
```

### JSON
```python
# Read JSON
con.execute("SELECT * FROM 'data.json'")

# Write JSON
con.execute("COPY table TO 'output.json'")
```

### Arrow
```python
# Read Arrow
con.execute("SELECT * FROM 'data.arrow'")

# Write Arrow
con.execute("COPY table TO 'output.arrow' (FORMAT ARROW)")
```

## 🎯 Use Cases

### When to Use DuckDB

- **Analytics and Reporting**: Fast analytical queries
- **Data Science**: Integration with Python/pandas
- **ETL Processes**: Data transformation and loading
- **Local Analysis**: Analyze local files without server setup
- **Prototyping**: Quick data exploration and testing

### When NOT to Use DuckDB

- **High Concurrency**: Limited multi-user support
- **Real-time Transactions**: Not designed for OLTP workloads
- **Petabyte Scale**: Single-node limitations
- **Complex Security**: Limited security features

## 📚 Learning Path

1. **Setup**: [Getting Started Guide](Getting-Started.md)
2. **Basics**: [Lab 2: Basic Operations](../labs/lab-02-basic-operations.md)
3. **Advanced**: [Lab 3: Advanced Features](../labs/lab-03-advanced-features.md)
4. **Integration**: [Lab 4: Python Integration](../labs/lab-04-python-integration.md)
5. **Performance**: [Lab 6: Performance & Optimization](../labs/lab-06-performance-optimization.md)

---

**Now you're ready to start learning DuckDB! Begin with [Lab 0: Sample Database Setup](../labs/lab-00-sample-database.md).**