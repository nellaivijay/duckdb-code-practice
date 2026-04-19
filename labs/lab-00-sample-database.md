# Lab 0: Sample Database Setup

## 🎯 Learning Objectives

- Generate realistic sample data for hands-on learning
- Load sample data into DuckDB database
- Understand the sample database schema
- Practice basic queries on sample data

## 📋 Prerequisites

- Python 3.8+ installed
- DuckDB Python package installed
- Completed environment setup

## ⏱️ Estimated Time

20-30 minutes

## 🎓 Conceptual Background

The sample database provides realistic business data for learning DuckDB concepts. It includes:

- **Customers**: Customer dimension with segmentation
- **Products**: Product catalog with categories
- **Orders**: Order fact table with status tracking
- **Transactions**: Transaction details with payment methods
- **Events**: Web events for user engagement analysis

This data allows you to practice real-world scenarios without dealing with sensitive data.

## 🚀 Step-by-Step Instructions

### Step 1: Generate Sample Data

Generate sample data using the provided script:

```bash
python3 scripts/generate_sample_data.py
```

By default, this generates:
- 1,000 customers
- 200 products
- 5,000 orders
- 10,000 transactions
- 20,000 events

You can customize the size:

```bash
# Small dataset
python3 scripts/generate_sample_data.py --size small

# Large dataset
python3 scripts/generate_sample_data.py --size large
```

### Step 2: Load Sample Data into DuckDB

Load the generated data into DuckDB:

```bash
python3 scripts/load_sample_data.py
```

This will:
- Create database schema
- Load data from Parquet files
- Create indexes for performance
- Verify data integrity

### Step 3: Verify Data Loading

Connect to the database and verify data:

```python
import duckdb

# Connect to database
con = duckdb.connect('data/duckdb_practice.db')

# Check table counts
tables = ['sample_customers', 'sample_products', 'sample_orders', 
          'sample_transactions', 'sample_events']

for table in tables:
    result = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    print(f"{table}: {result[0]} rows")
```

### Step 4: Explore Sample Data

Practice basic queries on the sample data:

```python
# View customer segments
con.execute("""
    SELECT segment, COUNT(*) as count 
    FROM sample_customers 
    GROUP BY segment 
    ORDER BY count DESC
""").fetchall()

# View product categories
con.execute("""
    SELECT category, COUNT(*) as count 
    FROM sample_products 
    GROUP BY category 
    ORDER BY count DESC
""").fetchall()

# View order status distribution
con.execute("""
    SELECT status, COUNT(*) as count 
    FROM sample_orders 
    GROUP BY status 
    ORDER BY count DESC
""").fetchall()
```

## 💻 Hands-On Exercises

### Exercise 1: Explore Customer Data

Write a query to find:
- Top 5 cities by customer count
- Customer distribution by segment
- Active vs inactive customer ratio

```python
# Your code here
```

### Exercise 2: Explore Product Data

Write a query to find:
- Products with highest stock quantities
- Products by price range
- Available vs unavailable product count

```python
# Your code here
```

### Exercise 3: Explore Order Data

Write a query to find:
- Total revenue by status
- Average order value
- Orders by payment method

```python
# Your code here
```

### Exercise 4: Explore Transaction Data

Write a query to find:
- Transaction success rate
- Total transaction amount by payment method
- Transactions by day of week

```python
# Your code here
```

### Exercise 5: Explore Event Data

Write a query to find:
- Event type distribution
- Events by device type
- Peak activity hours

```python
# Your code here
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Have sample data files in `data/sample/` directory
2. ✅ Have a DuckDB database at `data/duckdb_practice.db`
3. ✅ Be able to query all sample tables
4. ✅ Understand the sample database schema
5. ✅ Be ready to proceed to Lab 1

## 🔍 Verification

Verify your setup by running:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Verify all tables exist and have data
tables = con.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

# Verify row counts
for table in tables:
    table_name = table[0]
    count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"{table_name}: {count} rows")
```

Expected output:
```
Tables: [('sample_customers',), ('sample_products',), ('sample_orders',), ('sample_transactions',), ('sample_events',)]
sample_customers: 1000 rows
sample_products: 200 rows
sample_orders: 5000 rows
sample_transactions: 10000 rows
sample_events: 20000 rows
```

## 🆘 Troubleshooting

### Issue: Sample data generation fails

**Solution**: Ensure you have pandas and numpy installed:
```bash
pip install pandas numpy
```

### Issue: Database loading fails

**Solution**: Check that sample data files exist:
```bash
ls -la data/sample/
```

### Issue: DuckDB connection fails

**Solution**: Ensure the data directory exists:
```bash
mkdir -p data
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 1**: Environment Setup and Validation
2. **Learn DuckDB fundamentals**: Read DuckDB documentation
3. **Practice SQL**: Try different queries on sample data

---

**Your sample database is now ready for learning!**