# Lab 4: DuckDB + Python Integration

## 🎯 Learning Objectives

- Master DuckDB Python API for programmatic access
- Integrate DuckDB with pandas for data analysis
- Use DuckDB with NumPy arrays
- Implement data processing pipelines
- Handle transactions and error management
- Build lakehouse data pipelines with Python

## 📋 Prerequisites

- Completed Lab 3: Advanced Features
- Python 3.8+ with pandas and numpy installed
- Working DuckDB environment
- Sample database loaded

## ⏱️ Estimated Time

45-60 minutes

## 🎓 Conceptual Background

DuckDB's Python integration enables seamless data analysis and pipeline development. This lab covers:

**Python API**: Direct database access from Python
**Pandas Integration**: Zero-copy data transfer between DuckDB and pandas
**NumPy Integration**: Efficient array operations
**Transaction Management**: ACID compliance and error handling
**Pipeline Development**: Building robust data processing workflows
**Lakehouse Integration**: Python's role in modern lakehouse architectures

## 🚀 Step-by-Step Instructions

### Step 1: DuckDB Python API Basics

Master the fundamental Python API operations.

```python
import duckdb

# Connection management
con = duckdb.connect('data/duckdb_practice.db')
print("Connected to database")

# Basic query execution
result = con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()
print(f"Total customers: {result[0]}")

# Fetch all results
results = con.execute("SELECT * FROM sample_customers LIMIT 5").fetchall()
print("Sample customers:", results)

# Fetch single result
single = con.execute("SELECT AVG(loyalty_points) FROM sample_customers").fetchone()
print(f"Average loyalty points: {single[0]}")

# Execute with parameters
result = con.execute(
    "SELECT * FROM sample_customers WHERE segment = ?", 
    ['Premium']
).fetchall()
print(f"Premium customers: {len(result)}")

# Using context manager for automatic cleanup
with duckdb.connect('data/duckdb_practice.db') as con:
    result = con.execute("SELECT COUNT(*) FROM sample_products").fetchone()
    print(f"Total products: {result[0]}")
# Connection automatically closed
```

### Step 2: Pandas Integration

Leverage DuckDB's zero-copy integration with pandas.

```python
import duckdb
import pandas as pd

con = duckdb.connect('data/duckdb_practice.db')

# Query directly to DataFrame
df = con.execute("SELECT * FROM sample_customers LIMIT 10").df()
print("DataFrame shape:", df.shape)
print("DataFrame columns:", df.columns.tolist())
print("Sample data:")
print(df.head())

# Register pandas DataFrame with DuckDB
df_customers = con.execute("SELECT * FROM sample_customers").df()
con.register('customer_df', df_customers)

# Query registered DataFrame
result = con.execute("SELECT COUNT(*) FROM customer_df").fetchone()
print(f"Registered DataFrame rows: {result[0]}")

# Query with DataFrame and SQL together
result = con.execute("""
    SELECT c.segment, COUNT(*) as count
    FROM customer_df c
    GROUP BY c.segment
""").fetchdf()
print("Customer segments:")
print(result)

# Convert query results to pandas
df_analysis = con.execute("""
    SELECT segment, 
           COUNT(*) as customer_count,
           AVG(loyalty_points) as avg_loyalty,
           MAX(loyalty_points) as max_loyalty
    FROM sample_customers
    GROUP BY segment
""").df()
print("Segment analysis:")
print(df_analysis)

# Use DuckDB to query pandas DataFrames
df_orders = con.execute("SELECT * FROM sample_orders").df()
df_products = con.execute("SELECT * FROM sample_products").df()

# Complex analysis combining DataFrames
result = con.execute("""
    SELECT 
        o.order_id,
        o.total_amount,
        p.category,
        p.price
    FROM df_orders o
    JOIN df_products p ON o.product_id = p.product_id
    WHERE o.status = 'delivered'
    LIMIT 5
""").df()
print("Order-product analysis:")
print(result)
```

### Step 3: NumPy Integration

Work efficiently with NumPy arrays and DuckDB.

```python
import duckdb
import numpy as np

con = duckdb.connect('data/duckdb_practice.db')

# Query results as NumPy arrays
result = con.execute("SELECT loyalty_points FROM sample_customers").fetchall()
loyalty_array = np.array(result)
print("Loyalty points array shape:", loyalty_array.shape)
print("Mean loyalty points:", np.mean(loyalty_array))
print("Median loyalty points:", np.median(loyalty_array))

# Statistical analysis
print("Standard deviation:", np.std(loyalty_array))
print("Percentiles:")
print("25th percentile:", np.percentile(loyalty_array, 25))
print("50th percentile:", np.percentile(loyalty_array, 50))
print("75th percentile:", np.percentile(loyalty_array, 75))

# NumPy array operations
high_value_customers = loyalty_array[loyalty_array > 5000]
print(f"High-value customers: {len(high_value_customers)}")

# Create NumPy array and insert into DuckDB
new_data = np.array([
    (1001, 'New Customer', 'new@example.com', 'Standard', 1000, True),
    (1002, 'Another Customer', 'another@example.com', 'Premium', 5000, True)
])

# Insert array data
con.execute("""
    INSERT INTO sample_customers 
    (customer_id, first_name, email, segment, loyalty_points, is_active)
    VALUES (?, ?, ?, ?, ?, ?)
""", new_data.tolist())

print("Inserted new customers from NumPy array")

# Verify insertion
result = con.execute("""
    SELECT COUNT(*) FROM sample_customers WHERE customer_id >= 1001
""").fetchone()
print(f"New customers added: {result[0]}")
```

### Step 4: Transaction Management

Implement ACID transactions for data integrity.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Start transaction
con.begin()

try:
    # Multiple operations within transaction
    con.execute("""
        INSERT INTO sample_customers 
        (customer_id, first_name, email, segment, loyalty_points, is_active)
        VALUES (2001, 'Transaction Test', 'trans@example.com', 'Standard', 1500, True)
    """)
    
    con.execute("""
        INSERT INTO sample_orders 
        (order_id, customer_id, product_id, order_date, quantity, unit_price, total_amount, status, payment_method)
        VALUES (6001, 2001, 1, CURRENT_DATE, 2, 99.99, 199.98, 'pending', 'credit_card')
    """)
    
    # Commit transaction
    con.commit()
    print("Transaction committed successfully")
    
except Exception as e:
    # Rollback on error
    con.rollback()
    print(f"Transaction rolled back due to error: {e}")

# Verify transaction
result = con.execute("SELECT COUNT(*) FROM sample_customers WHERE customer_id = 2001").fetchone()
print(f"Customer 2001 exists: {result[0] > 0}")

# Transaction with savepoints
con.begin()
try:
    con.execute("INSERT INTO sample_customers VALUES (2002, 'Savepoint Test', 'save@example.com', 'Basic', 500, True)")
    
    # Create savepoint
    con.execute("SAVEPOINT sp1")
    
    con.execute("INSERT INTO sample_customers VALUES (2003, 'After Savepoint', 'after@example.com', 'Basic', 600, True)")
    
    # Rollback to savepoint
    con.execute("ROLLBACK TO SAVEPOINT sp1")
    
    con.commit()
    print("Transaction with savepoint completed")
    
except Exception as e:
    con.rollback()
    print(f"Transaction failed: {e}")

# Verify savepoint behavior
result = con.execute("SELECT COUNT(*) FROM sample_customers WHERE customer_id IN (2002, 2003)").fetchone()
print(f"Customers after savepoint: {result[0]}")  # Should be 1 (2002 exists, 2003 doesn't)
```

### Step 5: Data Processing Pipelines

Build robust data processing workflows.

```python
import duckdb
import pandas as pd
from datetime import datetime, timedelta

con = duckdb.connect('data/duckdb_practice.db')

# Pipeline 1: Data Quality Check
def data_quality_check(con, table_name):
    """Perform data quality checks on a table"""
    checks = {
        'row_count': con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0],
        'null_check': con.execute(f"""
            SELECT COUNT(*) FROM {table_name} 
            WHERE customer_id IS NULL
        """).fetchone()[0],
        'duplicate_check': con.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT customer_id) 
            FROM {table_name}
        """).fetchone()[0]
    }
    return checks

print("Data quality check for sample_customers:")
print(data_quality_check(con, 'sample_customers'))

# Pipeline 2: Data Transformation
def transform_customer_data(con):
    """Transform customer data for analysis"""
    df = con.execute("""
        SELECT 
            customer_id,
            first_name || ' ' || last_name as full_name,
            segment,
            loyalty_points,
            CASE 
                WHEN loyalty_points > 5000 THEN 'Gold'
                WHEN loyalty_points > 2000 THEN 'Silver'
                ELSE 'Bronze'
            END as loyalty_tier,
            is_active,
            registration_date
        FROM sample_customers
    """).df()
    return df

transformed_customers = transform_customer_data(con)
print("Transformed customer data:")
print(transformed_customers.head())

# Pipeline 3: Aggregation Pipeline
def daily_sales_pipeline(con, start_date, end_date):
    """Generate daily sales metrics"""
    df = con.execute(f"""
        SELECT 
            order_date,
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers,
            SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders
        FROM sample_orders
        WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY order_date
        ORDER BY order_date
    """).df()
    return df

# Generate last 30 days of sales data
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)
daily_sales = daily_sales_pipeline(con, start_date, end_date)
print("Daily sales pipeline:")
print(daily_sales.head())

# Pipeline 4: Lakehouse ETL Pattern
def lakehouse_etl_pipeline(con):
    """Implement lakehouse ETL pattern with bronze, silver, gold layers"""
    
    # Bronze layer: Raw data extraction
    bronze = con.execute("""
        SELECT * FROM sample_orders
        WHERE order_date >= '2022-01-01'
    """).df()
    print(f"Bronze layer: {len(bronze)} records")
    
    # Silver layer: Data validation and cleaning
    silver = con.execute("""
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
    """).df()
    print(f"Silver layer: {len(silver)} records")
    
    # Register silver layer for gold processing
    con.register('silver_orders', silver)
    
    # Gold layer: Business metrics and aggregations
    gold = con.execute("""
        SELECT 
            DATE_TRUNC('month', order_date) as month,
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers,
            SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
            ROUND(SUM(total_amount) / COUNT(DISTINCT customer_id), 2) as revenue_per_customer
        FROM silver_orders
        WHERE total_amount IS NOT NULL
        GROUP BY month
        ORDER BY month
    """).df()
    print(f"Gold layer: {len(gold)} months")
    
    return bronze, silver, gold

bronze, silver, gold = lakehouse_etl_pipeline(con)
print("Gold layer metrics:")
print(gold)
```

### Step 6: Error Handling and Logging

Implement robust error handling and logging.

```python
import duckdb
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def safe_query_execution(con, query, description=""):
    """Execute query with error handling and logging"""
    try:
        logger.info(f"Executing: {description}")
        result = con.execute(query).fetchdf()
        logger.info(f"Query successful: {len(result)} rows returned")
        return result
    except duckdb.Error as e:
        logger.error(f"Database error in {description}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in {description}: {e}")
        raise

def pipeline_with_error_handling(con):
    """Execute pipeline with comprehensive error handling"""
    try:
        logger.info("Starting data pipeline")
        
        # Step 1: Data extraction
        customers = safe_query_execution(
            con, 
            "SELECT * FROM sample_customers LIMIT 100",
            "Customer data extraction"
        )
        
        # Step 2: Data transformation
        transformed = safe_query_execution(
            con,
            """
            SELECT 
                customer_id,
                first_name,
                segment,
                loyalty_points,
                CASE 
                    WHEN loyalty_points > 5000 THEN 'High'
                    WHEN loyalty_points > 2000 THEN 'Medium'
                    ELSE 'Low'
                END as loyalty_category
            FROM sample_customers
            LIMIT 100
            """,
            "Customer data transformation"
        )
        
        # Step 3: Data loading (aggregation)
        aggregated = safe_query_execution(
            con,
            """
            SELECT 
                segment,
                COUNT(*) as customer_count,
                AVG(loyalty_points) as avg_loyalty
            FROM sample_customers
            GROUP BY segment
            """,
            "Customer data aggregation"
        )
        
        logger.info("Pipeline completed successfully")
        return customers, transformed, aggregated
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        # Implement recovery logic here
        raise

# Execute pipeline with error handling
try:
    customers, transformed, aggregated = pipeline_with_error_handling(con)
    print("Pipeline completed successfully")
    print("Aggregated results:")
    print(aggregated)
except Exception as e:
    print(f"Pipeline failed: {e}")
```

## 💻 Hands-On Exercises

### Exercise 1: Build Customer Analytics Pipeline

Create a complete customer analytics pipeline:

```python
# Your code here
# Extract customer data
# Transform and clean data
# Calculate customer metrics
# Create customer segments
# Generate insights
```

### Exercise 2: Implement Data Quality Framework

Build a comprehensive data quality checking system:

```python
# Your code here
# Define quality rules
# Implement validation checks
# Generate quality reports
# Handle quality issues
# Create alerts
```

### Exercise 3: Lakehouse Pipeline Development

Develop a complete lakehouse ETL pipeline:

```python
# Your code here
# Bronze layer extraction
# Silver layer transformation
# Gold layer aggregation
# Data quality checks
# Metadata management
```

### Exercise 4: Real-time Data Processing

Build a real-time data processing simulation:

```python
# Your code here
# Simulate real-time data ingestion
# Process streaming data
# Update metrics incrementally
# Handle late-arriving data
# Monitor pipeline health
```

### Exercise 5: Machine Learning Integration

Integrate DuckDB with machine learning workflows:

```python
# Your code here
# Extract features from DuckDB
# Prepare data for ML
# Train models on DuckDB data
# Store predictions back to DuckDB
# Create ML pipelines
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Be proficient with DuckDB Python API
2. ✅ Master pandas and NumPy integration
3. ✅ Implement robust transaction management
4. ✅ Build data processing pipelines
5. ✅ Handle errors and implement logging
6. ✅ Understand lakehouse pipeline patterns

## 🔍 Verification

Test your Python integration skills:

```python
import duckdb
import pandas as pd

con = duckdb.connect('data/duckdb_practice.db')

# Test Python API
result = con.execute("SELECT COUNT(*) FROM sample_customers").fetchone()
print(f"Python API test: {result[0]} customers")

# Test pandas integration
df = con.execute("SELECT * FROM sample_customers LIMIT 5").df()
print(f"Pandas integration test: {df.shape}")

# Test transaction
con.begin()
try:
    con.execute("INSERT INTO sample_customers VALUES (9999, 'Test', 'test@test.com', 'Basic', 100, True)")
    con.execute("ROLLBACK")
    print("Transaction test: PASSED")
except:
    print("Transaction test: FAILED")

print("✅ Python integration test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: Memory errors with large DataFrames

**Solution**: Process data in chunks:
```python
# Process in batches
chunk_size = 1000
for chunk in pd.read_sql("SELECT * FROM large_table", con, chunksize=chunk_size):
    # Process chunk
    pass
```

### Issue: Transaction conflicts

**Solution**: Use proper isolation levels and retry logic:
```python
# Implement retry logic
max_retries = 3
for attempt in range(max_retries):
    try:
        con.begin()
        # Your operations
        con.commit()
        break
    except:
        con.rollback()
        if attempt == max_retries - 1:
            raise
```

### Issue: Pandas performance

**Solution**: Use DuckDB for heavy operations, pandas for final formatting:
```python
# Let DuckDB handle heavy computation
result = con.execute("COMPLEX_QUERY").df()
# Use pandas for final formatting
result = result.pivot(...)
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 5**: Data Format Operations
2. **Build production pipelines**: Apply patterns to real data
3. **Study lakehouse patterns**: Deep dive into modern architecture
4. **Learn MLOps**: Integrate with machine learning workflows

---

**You now have comprehensive DuckDB Python integration skills for building production data pipelines!**