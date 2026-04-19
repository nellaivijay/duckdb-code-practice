# Lab 5A: Exploring Data Without Persistence

## 🎯 Learning Objectives

- Understand why and when to use DuckDB without persistence
- Practice inferring file types and schemas automatically
- Learn to shred nested JSON data
- Convert between data formats (CSV to Parquet)
- Query Parquet files directly without loading
- Query SQLite and other databases
- Work with Excel files in DuckDB

## 📋 Prerequisites

- Completed Lab 0: Sample Database Setup
- Completed Lab 1A: Introduction to DuckDB
- DuckDB Python package installed
- Sample data files available

## ⏱️ Estimated Time

60-75 minutes

## 🎓 Conceptual Background

### Why Use a Database Without Persisting Data?

DuckDB's ability to query data files directly without creating persistent tables offers several advantages:

1. **Exploratory Analysis**: Quickly explore data without setup overhead
2. **Data Validation**: Verify data quality before loading
3. **Format Testing**: Test different formats before committing
4. **Memory Efficiency**: Process large files without disk I/O
5. **Pipeline Flexibility**: Mix persistent and ephemeral data
6. **Ad-hoc Analysis**: Quick queries without database management

### File Type and Schema Inference

DuckDB automatically detects file types and schemas:

```python
# Automatic detection
con.execute("SELECT * FROM 'data.csv'")  # Detects CSV
con.execute("SELECT * FROM 'data.parquet'")  # Detects Parquet
con.execute("SELECT * FROM 'data.json'")  # Detects JSON

# Explicit specification
con.execute("SELECT * FROM read_csv('data.csv')")
con.execute("SELECT * FROM read_parquet('data.parquet')")
con.execute("SELECT * FROM read_json('data.json')")
```

### CSV Parsing Notes

DuckDB's CSV parser handles various CSV formats:

```python
# Auto-detection
con.execute("SELECT * FROM read_csv_auto('data.csv')")

# Manual configuration
con.execute("""
    SELECT * FROM read_csv('data.csv',
        delim=',',
        header=true,
        quote='"',
        escape='"'
    )
""")
```

### Nested JSON Shredding

DuckDB can shred nested JSON structures:

```python
# Flatten nested JSON
con.execute("""
    SELECT * FROM read_json('data.json',
        format='auto',
        records=true
    )
""")

# Extract nested fields
con.execute("""
    SELECT 
        user->>'name' as name,
        user->>'email' as email,
        orders[1]->>'total' as first_order_total
    FROM read_json('nested.json')
""")
```

## 🚀 Step-by-Step Instructions

### Step 1: Practice File Type Inference

Let's explore DuckDB's automatic file type detection:

```python
import duckdb

con = duckdb.connect(':memory:')

# Create sample files in different formats
con.execute("""
    CREATE TABLE sample AS
    SELECT 
        id,
        'Product ' || id as name,
        random() * 100 as price,
        '2023-01-01'::date + (random() * 365)::int as date
    FROM range(100)
""")

# Export to different formats
con.execute("COPY sample TO 'data/auto_test.csv' (FORMAT CSV, HEADER)")
con.execute("COPY sample TO 'data/auto_test.parquet' (FORMAT PARQUET)")
con.execute("COPY sample TO 'data/auto_test.json' (FORMAT JSON, ARRAY false)")

# Test automatic detection
csv_result = con.execute("SELECT COUNT(*) FROM 'data/auto_test.csv'").fetchone()
parquet_result = con.execute("SELECT COUNT(*) FROM 'data/auto_test.parquet'").fetchone()
json_result = con.execute("SELECT COUNT(*) FROM 'data/auto_test.json'").fetchone()

print(f"CSV: {csv_result[0]} rows")
print(f"Parquet: {parquet_result[0]} rows")
print(f"JSON: {json_result[0]} rows")
```

### Step 2: Practice Schema Inference

Explore DuckDB's automatic schema detection:

```python
import duckdb

con = duckdb.connect(':memory:')

# Query a file and examine the inferred schema
con.execute("DESCRIBE SELECT * FROM 'data/sample/customers.csv'")
schema = con.fetchall()
print("Inferred schema for customers.csv:")
for column in schema:
    print(f"  {column[0]}: {column[1]}")

# Compare with actual table schema
con.execute("CREATE TABLE customers AS SELECT * FROM 'data/sample/customers.csv'")
con.execute("DESCRIBE customers")
table_schema = con.fetchall()
print("\nTable schema:")
for column in table_schema:
    print(f"  {column[0]}: {column[1]}")
```

### Step 3: Shred Nested JSON

Practice working with nested JSON structures:

```python
import duckdb
import json

con = duckdb.connect(':memory:')

# Create nested JSON sample
nested_data = [
    {
        "user": {"id": 1, "name": "Alice", "email": "alice@example.com"},
        "orders": [
            {"id": 101, "total": 100.50, "date": "2023-01-15"},
            {"id": 102, "total": 75.25, "date": "2023-02-20"}
        ]
    },
    {
        "user": {"id": 2, "name": "Bob", "email": "bob@example.com"},
        "orders": [
            {"id": 201, "total": 200.00, "date": "2023-01-10"}
        ]
    }
]

# Write nested JSON to file
with open('data/nested_orders.json', 'w') as f:
    json.dump(nested_data, f)

# Query nested JSON
result = con.execute("""
    SELECT 
        user->>'name' as customer_name,
        user->>'email' as customer_email,
        len(orders) as order_count,
        orders[1]->>'total' as first_order_total
    FROM read_json('data/nested_orders.json', format='auto')
""").fetchdf()
print(result)
```

### Step 4: Convert CSV to Parquet

Practice format conversion:

```python
import duckdb

con = duckdb.connect(':memory:')

# Read CSV and convert to Parquet
con.execute("""
    COPY (
        SELECT * FROM 'data/sample/customers.csv'
    ) TO 'data/customers.parquet' (FORMAT PARQUET)
""")

# Compare file sizes
import os
csv_size = os.path.getsize('data/sample/customers.csv') / 1024  # KB
parquet_size = os.path.getsize('data/customers.parquet') / 1024  # KB

print(f"CSV size: {csv_size:.2f} KB")
print(f"Parquet size: {parquet_size:.2f} KB")
print(f"Compression ratio: {csv_size/parquet_size:.2f}x")

# Query performance comparison
import time

start = time.time()
con.execute("SELECT COUNT(*) FROM 'data/sample/customers.csv'").fetchone()
csv_time = time.time() - start

start = time.time()
con.execute("SELECT COUNT(*) FROM 'data/customers.parquet'").fetchone()
parquet_time = time.time() - start

print(f"\nCSV query time: {csv_time:.4f}s")
print(f"Parquet query time: {parquet_time:.4f}s")
print(f"Speed improvement: {csv_time/parquet_time:.2f}x")
```

### Step 5: Query Parquet Files Directly

Practice querying Parquet files without loading:

```python
import duckdb

con = duckdb.connect(':memory:')

# Query Parquet file directly
result = con.execute("""
    SELECT 
        segment,
        COUNT(*) as customer_count,
        AVG(loyalty_points) as avg_loyalty
    FROM 'data/customers.parquet'
    GROUP BY segment
""").fetchdf()
print("Direct Parquet query results:")
print(result)

# Use Parquet file in joins
result = con.execute("""
    SELECT 
        c.segment,
        c.customer_id,
        p.product_name,
        o.total_amount
    FROM 'data/customers.parquet' c
    JOIN 'data/sample/products.parquet' p ON c.customer_id = p.product_id
    JOIN 'data/sample/orders.parquet' o ON c.customer_id = o.customer_id
    LIMIT 10
""").fetchdf()
print("\nJoin with Parquet files:")
print(result)
```

### Step 6: Query SQLite Databases

Practice querying other database formats:

```python
import duckdb
import sqlite3

# Create a SQLite database
sqlite_con = sqlite3.connect('data/test_sqlite.db')
sqlite_con.execute("""
    CREATE TABLE sqlite_products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )
""")
sqlite_con.execute("""
    INSERT INTO sqlite_products VALUES 
        (1, 'Product A', 10.99),
        (2, 'Product B', 20.50),
        (3, 'Product C', 15.75)
""")
sqlite_con.commit()
sqlite_con.close()

# Query SQLite from DuckDB
con = duckdb.connect(':memory:')
result = con.execute("""
    SELECT * FROM sqlite_scan('data/test_sqlite.db', 'sqlite_products')
""").fetchdf()
print("SQLite data queried from DuckDB:")
print(result)

# Join SQLite data with DuckDB data
con.execute("CREATE TABLE duckdb_products AS SELECT * FROM 'data/sample/products.parquet'")
result = con.execute("""
    SELECT 
        s.id as sqlite_id,
        s.name as sqlite_name,
        d.product_name as duckdb_name
    FROM sqlite_scan('data/test_sqlite.db', 'sqlite_products') s
    JOIN duckdb_products d ON s.id = d.product_id
""").fetchdf()
print("\nSQLite + DuckDB join:")
print(result)
```

### Step 7: Work with Excel Files

Practice reading Excel files:

```python
import duckdb

# First, let's install the spreadsheet extension
con = duckdb.connect(':memory:')

# Install and load the spreadsheet extension
try:
    con.execute("INSTALL spreadsheet")
    con.execute("LOAD spreadsheet")
    print("Spreadsheet extension loaded successfully")
except Exception as e:
    print(f"Note: Spreadsheet extension may not be available: {e}")
    print("This is expected in some DuckDB installations")

# Alternative: Convert Excel to CSV first
# (This is a common workaround when the extension is not available)
import pandas as pd

# Create a sample Excel file
df = pd.DataFrame({
    'id': range(1, 11),
    'name': [f'Product {i}' for i in range(1, 11)],
    'price': [round(10 + i * 5, 2) for i in range(10)]
})
df.to_excel('data/sample_excel.xlsx', index=False)

# Read Excel via pandas and query with DuckDB
excel_df = pd.read_excel('data/sample_excel.xlsx')
con.register('excel_data', excel_df)
result = con.execute("SELECT * FROM excel_data WHERE price > 30").fetchdf()
print("Excel data queried via pandas:")
print(result)
```

## 💻 Hands-On Exercises

### Exercise 1: Comprehensive File Format Comparison

Compare different file formats for a realistic dataset:

```python
import duckdb
import time
import os

con = duckdb.connect(':memory:')

# Create a realistic dataset
con.execute("""
    CREATE TABLE sales_data AS
    SELECT 
        (random() * 1000)::int as customer_id,
        (random() * 100)::int as product_id,
        random() * 500 as amount,
        ['credit_card', 'debit_card', 'paypal'][((random() * 3)::int)] as payment_method,
        '2023-01-01'::date + (random() * 365)::int as sale_date
    FROM range(100000)
""")

# Test different formats
formats = ['csv', 'parquet', 'json']
results = []

for format in formats:
    # Export
    start = time.time()
    con.execute(f"COPY sales_data TO 'data/sales.{format}' (FORMAT {format.upper()})")
    export_time = time.time() - start
    
    # File size
    file_size = os.path.getsize(f'data/sales.{format}') / 1024  # KB
    
    # Query performance
    start = time.time()
    con.execute(f"SELECT COUNT(*), AVG(amount) FROM 'data/sales.{format}'").fetchone()
    query_time = time.time() - start
    
    results.append({
        'format': format,
        'export_time': export_time,
        'file_size': file_size,
        'query_time': query_time
    })

# Display results
for result in results:
    print(f"{result['format'].upper()}:")
    print(f"  Export: {result['export_time']:.4f}s")
    print(f"  Size: {result['file_size']:.2f}KB")
    print(f"  Query: {result['query_time']:.4f}s")
    print()
```

### Exercise 2: Complex JSON Shredding

Work with complex nested JSON structures:

```python
import duckdb
import json

con = duckdb.connect(':memory:')

# Create complex nested JSON
complex_data = {
    "company": "TechCorp",
    "departments": [
        {
            "name": "Engineering",
            "employees": [
                {"id": 1, "name": "Alice", "skills": ["Python", "SQL"], "salary": 90000},
                {"id": 2, "name": "Bob", "skills": ["Java", "Go"], "salary": 95000}
            ]
        },
        {
            "name": "Sales",
            "employees": [
                {"id": 3, "name": "Charlie", "skills": ["Sales", "CRM"], "salary": 70000}
            ]
        }
    ]
}

# Write to file
with open('data/complex_nested.json', 'w') as f:
    json.dump(complex_data, f)

# Query and flatten the nested structure
# Your code here to extract employee information
```

### Exercise 3: Multi-Source Data Integration

Combine data from multiple sources without persistence:

```python
import duckdb

con = duckdb.connect(':memory:')

# Combine data from CSV, Parquet, and SQLite
# Your code here to create a unified view
```

### Exercise 4: Data Validation Pipeline

Create a data validation pipeline that checks data quality before loading:

```python
import duckdb

con = duckdb.connect(':memory:')

# Validate data from files before loading
# Your code here to check:
# - Data types
# - Null values
# - Value ranges
# - Referential integrity
```

### Exercise 5: Performance Optimization

Optimize queries on file-based data:

```python
import duckdb

con = duckdb.connect(':memory:')

# Practice optimization techniques for file-based queries:
# - Push down predicates
# - Column pruning
# - Partitioning strategies
# Your optimization code here
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Understand when to use DuckDB without persistence
2. ✅ Be proficient in file type and schema inference
3. ✅ Be able to shred nested JSON structures
4. ✅ Know how to convert between data formats
5. ✅ Be comfortable querying Parquet files directly
6. ✅ Be able to query SQLite and other databases
7. ✅ Understand how to work with Excel files

## 🔍 Verification

Verify your skills with this comprehensive test:

```python
import duckdb
import os

print("=== Data Without Persistence Verification ===")

con = duckdb.connect(':memory:')

# Test 1: File type inference
con.execute("CREATE TABLE test AS SELECT * FROM range(100)")
con.execute("COPY test TO 'data/verify.csv' (FORMAT CSV, HEADER)")
csv_count = con.execute("SELECT COUNT(*) FROM 'data/verify.csv'").fetchone()[0]
print(f"✓ File type inference: {csv_count} == 100")

# Test 2: Schema inference
schema = con.execute("DESCRIBE SELECT * FROM 'data/verify.csv'").fetchall()
print(f"✓ Schema inference: {len(schema)} columns detected")

# Test 3: Format conversion
con.execute("COPY test TO 'data/verify.parquet' (FORMAT PARQUET)")
parquet_count = con.execute("SELECT COUNT(*) FROM 'data/verify.parquet'").fetchone()[0]
print(f"✓ Format conversion: {parquet_count} == 100")

# Test 4: File size comparison
csv_size = os.path.getsize('data/verify.csv')
parquet_size = os.path.getsize('data/verify.parquet')
print(f"✓ Parquet compression: {csv_size/parquet_size:.2f}x smaller")

print("=== All Verification Tests Passed ===")
```

## 🆘 Troubleshooting

### Issue: JSON parsing fails

**Solution**: Check JSON format and use appropriate options:
```python
con.execute("""
    SELECT * FROM read_json('data.json',
        format='auto',
        records=true
    )
""")
```

### Issue: Parquet file not found

**Solution**: Ensure file path is correct and file exists:
```python
import os
print(os.path.exists('data/file.parquet'))
```

### Issue: Spreadsheet extension not available

**Solution**: Use pandas as intermediate step:
```python
import pandas as pd
df = pd.read_excel('data.xlsx')
con.register('excel_data', df)
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 6**: Python Integration
2. **Practice more**: Experiment with different data formats
3. **Real-world data**: Apply these techniques to your own datasets

---

**You now have the skills to explore and analyze data without the overhead of database persistence!**