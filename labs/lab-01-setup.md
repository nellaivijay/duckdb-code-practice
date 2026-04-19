# Lab 1: Environment Setup

## 🎯 Learning Objectives

- Verify DuckDB installation and configuration
- Test database connectivity
- Explore different DuckDB interfaces (Python API, SQL shell)
- Validate Jupyter notebook setup
- Understand DuckDB configuration options

## 📋 Prerequisites

- Completed Lab 0: Sample Database Setup
- Python 3.8+ installed
- Jupyter notebook installed

## ⏱️ Estimated Time

30-45 minutes

## 🎓 Conceptual Background

DuckDB can be used through multiple interfaces:

1. **Python API**: Programmatic access using the `duckdb` package
2. **SQL Shell**: Interactive command-line interface
3. **Jupyter Notebooks**: Interactive analysis environment
4. **Embedded Mode**: In-memory database for applications

Each interface has its strengths and use cases. In this lab, you'll explore all of them.

## 🚀 Step-by-Step Instructions

### Step 1: Verify DuckDB Installation

Check that DuckDB is properly installed:

```python
import duckdb
print(f"DuckDB version: {duckdb.__version__}")
```

Expected output: DuckDB version number (e.g., 0.9.0)

### Step 2: Test Python API

Connect to the sample database using the Python API:

```python
import duckdb

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Test basic query
result = con.execute("SELECT 1 as test").fetchall()
print(f"Test query result: {result}")

# Test sample data query
customers = con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()
print(f"Customer count: {customers[0]}")

# Close connection
con.close()
```

### Step 3: Test SQL Shell

DuckDB provides a command-line SQL shell. Test it:

```bash
# Start DuckDB shell
duckdb data/duckdb_practice.db

# In the shell, run:
SELECT COUNT(*) FROM sample_customers;
SELECT * FROM sample_products LIMIT 5;

# Exit the shell
.exit
```

### Step 4: Test Jupyter Integration

Start Jupyter notebook:

```bash
jupyter notebook
```

In a Jupyter notebook cell:

```python
import duckdb
import pandas as pd

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Query and convert to pandas DataFrame
df = con.execute("SELECT * FROM sample_customers LIMIT 10").df()
print(df.head())

# Close connection
con.close()
```

### Step 5: Explore DuckDB Configuration

DuckDB has many configuration options. Explore some key settings:

```python
import duckdb

con = duckdb.connect(':memory:')

# View current configuration
config = con.execute("SELECT * FROM duckdb_settings()").fetchall()
print("Current DuckDB settings:")
for setting in config[:10]:  # Show first 10 settings
    print(f"{setting[0]}: {setting[1]}")

# Set memory limit
con.execute("SET memory_limit='2GB'")
print("Memory limit set to 2GB")

# Set thread count
con.execute("SET threads=4")
print("Thread count set to 4")

# Enable progress bar
con.execute("SET enable_progress_bar=true")
print("Progress bar enabled")

con.close()
```

### Step 6: Test Different Connection Modes

DuckDB supports different connection modes:

```python
import duckdb

# In-memory database (ephemeral)
con_memory = duckdb.connect(':memory:')
print("In-memory database created")

# Persistent database
con_persistent = duckdb.connect('data/test.db')
print("Persistent database created")

# Read-only connection
con_readonly = duckdb.connect('data/duckdb_practice.db', read_only=True)
print("Read-only connection created")

# Close connections
con_memory.close()
con_persistent.close()
con_readonly.close()
```

## 💻 Hands-On Exercises

### Exercise 1: Practice Python API Operations

Using the Python API, perform the following:

```python
import duckdb

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# 1. Find the top 3 most expensive products
# Your code here

# 2. Calculate average order value
# Your code here

# 3. Find customers with most orders
# Your code here

# 4. Calculate total revenue by month
# Your code here

con.close()
```

### Exercise 2: Practice SQL Shell Queries

Using the DuckDB SQL shell, execute these queries:

```sql
-- 1. Find products in the 'Electronics' category
-- Your SQL here

-- 2. Calculate revenue by customer segment
-- Your SQL here

-- 3. Find orders with delivery date after order date
-- Your SQL here

-- 4. Count events by event type
-- Your SQL here
```

### Exercise 3: Jupyter Integration

In a Jupyter notebook, create a visualization:

```python
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Query data for visualization
# Your code here to get data for plotting

# Create a visualization
# Your code here to create a plot

con.close()
```

### Exercise 4: Configuration Exploration

Explore DuckDB configuration options:

```python
import duckdb

con = duckdb.connect(':memory:')

# Find all configuration options related to memory
# Your code here

# Find all configuration options related to threads
# Your code here

# Experiment with different settings
# Your code here

con.close()
```

### Exercise 5: Error Handling

Practice error handling with DuckDB:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Try to query a non-existent table
try:
    result = con.execute("SELECT * FROM non_existent_table").fetchall()
except Exception as e:
    print(f"Error: {e}")

# Try to insert invalid data
try:
    con.execute("INSERT INTO sample_customers VALUES (999, 'Test', 'User', 'invalid')")
except Exception as e:
    print(f"Error: {e}")

con.close()
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Have DuckDB properly installed and configured
2. ✅ Be able to connect to databases using Python API
3. ✅ Be able to use the DuckDB SQL shell
4. ✅ Have Jupyter notebook integration working
5. ✅ Understand different DuckDB connection modes
6. ✅ Be familiar with DuckDB configuration options

## 🔍 Verification

Verify your setup by running this comprehensive check:

```python
import duckdb
import sys

print("=== DuckDB Environment Verification ===")
print(f"Python version: {sys.version}")
print(f"DuckDB version: {duckdb.__version__}")

# Test Python API
print("\n=== Python API Test ===")
con = duckdb.connect('data/duckdb_practice.db')
result = con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()
print(f"✓ Python API working: {result[0]} customers found")

# Test configuration
print("\n=== Configuration Test ===")
con.execute("SET memory_limit='1GB'")
print("✓ Configuration setting successful")

# Test different connection modes
print("\n=== Connection Mode Test ===")
con_memory = duckdb.connect(':memory:')
print("✓ In-memory connection successful")
con_memory.close()

print("\n=== All Tests Passed ===")
con.close()
```

## 🆘 Troubleshooting

### Issue: DuckDB import fails

**Solution**: Install DuckDB:
```bash
pip install duckdb
```

### Issue: SQL shell not found

**Solution**: Install DuckDB CLI tools:
```bash
# On Ubuntu/Debian
sudo apt-get install duckdb

# On macOS
brew install duckdb

# Or use Python package
pip install duckdb
```

### Issue: Jupyter not starting

**Solution**: Install Jupyter:
```bash
pip install jupyter notebook
```

### Issue: Database connection fails

**Solution**: Check that the database file exists:
```bash
ls -la data/
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 2**: Basic Operations
2. **Read DuckDB documentation**: https://duckdb.org/docs/
3. **Practice SQL**: Try different queries on sample data

---

**Your DuckDB environment is now fully configured and ready for learning!**