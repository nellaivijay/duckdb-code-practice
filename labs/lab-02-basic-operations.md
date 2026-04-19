# Lab 2: Basic DuckDB Operations

## 🎯 Learning Objectives

- Create and manage DuckDB databases
- Create and modify tables
- Perform basic CRUD operations (Create, Read, Update, Delete)
- Understand DuckDB data types
- Practice basic SQL queries in DuckDB

## 📋 Prerequisites

- Completed Lab 1: Environment Setup
- Working DuckDB installation
- Sample database loaded

## ⏱️ Estimated Time

45-60 minutes

## 🎓 Conceptual Background

DuckDB supports standard SQL operations with some unique features:

**Data Types**: DuckDB supports various data types including INTEGER, VARCHAR, DATE, TIMESTAMP, and more.

**SQL Compatibility**: DuckDB is highly SQL-compliant and supports most standard SQL operations.

**Columnar Storage**: DuckDB uses columnar storage internally, which is optimized for analytical queries.

**In-Memory Processing**: DuckDB excels at in-memory processing for fast analytics.

## 🚀 Step-by-Step Instructions

### Step 1: Create a New Database

Create a new database for this lab:

```python
import duckdb

# Create a new database
con = duckdb.connect('data/lab2_practice.db')

# Verify connection
print("Database created successfully")
```

### Step 2: Create Tables

Create tables with different data types:

```python
# Create a simple table
con.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        department VARCHAR,
        salary INTEGER,
        hire_date DATE
    )
""")

# Create a table with various data types
con.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name VARCHAR,
        price DECIMAL(10,2),
        in_stock BOOLEAN,
        created_at TIMESTAMP
    )
""")

print("Tables created successfully")
```

### Step 3: Insert Data

Insert data into the tables:

```python
# Insert single row
con.execute("""
    INSERT INTO employees VALUES 
    (1, 'John Doe', 'Engineering', 75000, '2020-01-15')
""")

# Insert multiple rows
con.execute("""
    INSERT INTO employees VALUES 
    (2, 'Jane Smith', 'Marketing', 65000, '2019-03-22'),
    (3, 'Bob Johnson', 'Engineering', 80000, '2018-11-01'),
    (4, 'Alice Williams', 'Sales', 60000, '2021-06-10'),
    (5, 'Charlie Brown', 'Engineering', 70000, '2020-07-20')
""")

# Insert with explicit column names
con.execute("""
    INSERT INTO products (product_id, name, price, in_stock, created_at)
    VALUES 
    (1, 'Laptop', 999.99, true, '2023-01-01 10:00:00'),
    (2, 'Mouse', 29.99, true, '2023-01-02 11:00:00'),
    (3, 'Keyboard', 79.99, false, '2023-01-03 12:00:00')
""")

print("Data inserted successfully")
```

### Step 4: Query Data

Perform basic SELECT queries:

```python
# Select all columns
result = con.execute("SELECT * FROM employees").fetchall()
print("All employees:", result)

# Select specific columns
result = con.execute("SELECT name, department FROM employees").fetchall()
print("Employee names and departments:", result)

# Select with WHERE clause
result = con.execute("""
    SELECT * FROM employees 
    WHERE department = 'Engineering'
""").fetchall()
print("Engineering employees:", result)

# Select with ORDER BY
result = con.execute("""
    SELECT * FROM employees 
    ORDER BY salary DESC
""").fetchall()
print("Employees by salary (descending):", result)

# Select with LIMIT
result = con.execute("SELECT * FROM employees LIMIT 2").fetchall()
print("First 2 employees:", result)
```

### Step 5: Update Data

Update existing records:

```python
# Update single record
con.execute("""
    UPDATE employees 
    SET salary = 85000 
    WHERE id = 3
""")

# Update multiple records
con.execute("""
    UPDATE employees 
    SET salary = salary * 1.10 
    WHERE department = 'Engineering'
""")

print("Data updated successfully")
```

### Step 6: Delete Data

Delete records from tables:

```python
# Delete specific record
con.execute("""
    DELETE FROM products 
    WHERE product_id = 3
""")

# Delete with condition
con.execute("""
    DELETE FROM employees 
    WHERE id = 5
""")

print("Data deleted successfully")
```

### Step 7: Use Sample Database

Practice queries on the sample database:

```python
# Switch to sample database
con_sample = duckdb.connect('data/duckdb_practice.db')

# Basic queries
result = con_sample.execute("""
    SELECT * FROM sample_customers 
    WHERE segment = 'Premium' 
    LIMIT 5
""").fetchall()
print("Premium customers:", result)

# Aggregation
result = con_sample.execute("""
    SELECT segment, COUNT(*) as count, AVG(loyalty_points) as avg_points
    FROM sample_customers 
    GROUP BY segment
""").fetchall()
print("Customer segments:", result)

# Join
result = con_sample.execute("""
    SELECT c.first_name, c.last_name, o.order_date, o.total_amount
    FROM sample_customers c
    JOIN sample_orders o ON c.customer_id = o.customer_id
    LIMIT 5
""").fetchall()
print("Customer orders:", result)

con_sample.close()
```

## 💻 Hands-On Exercises

### Exercise 1: Table Creation

Create a table called `departments` with the following schema:
- department_id (INTEGER, PRIMARY KEY)
- department_name (VARCHAR)
- budget (INTEGER)
- location (VARCHAR)

```python
# Your code here
```

### Exercise 2: Data Insertion

Insert at least 5 departments into the departments table.

```python
# Your code here
```

### Exercise 3: Complex Queries

Write queries to:
1. Find all customers who registered in 2022
2. Calculate total revenue by product category
3. Find the top 3 customers by loyalty points
4. Count orders by status

```python
# Your code here
```

### Exercise 4: Data Modification

1. Update the price of all products in the 'Electronics' category by 10%
2. Set all pending orders to 'processing' status
3. Add 100 loyalty points to all active customers

```python
# Your code here
```

### Exercise 5: Data Type Practice

Create a table with various DuckDB data types and insert sample data:

```python
# Create table with different data types
# Your code here

# Insert sample data
# Your code here

# Query and verify data types
# Your code here
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Be able to create and manage DuckDB databases
2. ✅ Understand how to create tables with different data types
3. ✅ Be proficient in CRUD operations
4. ✅ Be able to write basic SQL queries
5. ✅ Understand DuckDB's SQL dialect

## 🔍 Verification

Verify your work by running:

```python
import duckdb

con = duckdb.connect('data/lab2_practice.db')

# Verify tables exist
tables = con.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

# Verify data counts
for table in tables:
    table_name = table[0]
    count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"{table_name}: {count} rows")

# Verify data integrity
result = con.execute("""
    SELECT COUNT(*) FROM employees 
    WHERE department = 'Engineering'
""").fetchone()
print(f"Engineering employees: {result[0]}")

con.close()
```

## 🆘 Troubleshooting

### Issue: Table creation fails

**Solution**: Check for syntax errors and ensure data types are correct:
```python
# Check table schema
con.execute("DESCRIBE employees").fetchall()
```

### Issue: Insert fails

**Solution**: Verify data types match table schema:
```python
# Check table schema first
con.execute("DESCRIBE employees").fetchall()
```

### Issue: Query returns no results

**Solution**: Verify data exists in the table:
```python
con.execute("SELECT COUNT(*) FROM table_name").fetchone()
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 3**: Advanced Features
2. **Practice SQL**: Try more complex queries
3. **Learn about joins**: Practice different join types

---

**You now have a solid foundation in DuckDB basic operations!**