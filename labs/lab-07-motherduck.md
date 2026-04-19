# Lab 7: DuckDB in the Cloud with MotherDuck

## 🎯 Learning Objectives

- Understand MotherDuck and its role in the DuckDB ecosystem
- Learn how MotherDuck works and its architecture
- Set up and configure MotherDuck account
- Connect to MotherDuck using the DuckDB CLI
- Use token-based authentication for programmatic access
- Upload and manage databases in MotherDuck
- Share databases with collaborators
- Configure S3 secrets and load data from S3 buckets
- Optimize data ingestion and MotherDuck usage
- Query data with AI assistance
- Explore MotherDuck integrations

## 📋 Prerequisites

- Completed Lab 0: Sample Database Setup
- Completed Lab 1A: Introduction to DuckDB
- DuckDB CLI installed
- MotherDuck account (free tier available)
- Internet connection for cloud services

## ⏱️ Estimated Time

75-90 minutes

## 🎓 Conceptual Background

### What is MotherDuck?

MotherDuck is a cloud-native data platform built on DuckDB that provides:

- **Cloud Storage**: Persistent storage for DuckDB databases
- **Collaboration**: Share databases with team members
- **Scalability**: Handle larger datasets than local machines
- **Integration**: Connect with various data sources and tools
- **Serverless**: No infrastructure management required
- **Compatibility**: Works with existing DuckDB workflows

### How MotherDuck Works

```
┌─────────────────────────────────────────────────────────────┐
│                    MotherDuck Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Local DuckDB          MotherDuck Cloud          External   │
│  ┌──────────┐         ┌──────────┐          ┌──────────┐  │
│  │ Local DB │◄────────│ Cloud DB │──────────▶│   S3     │  │
│  │          │         │          │          │  Buckets │  │
│  └──────────┘         └──────────┘          └──────────┘  │
│       │                    │                     │        │
│       │                    │                     │        │
│       ▼                    ▼                     ▼        │
│  ┌──────────┐         ┌──────────┐          ┌──────────┐  │
│  │ DuckDB   │         │ MotherDuck│         │  Other   │  │
│  │   CLI    │         │   UI     │          │  Tools   │  │
│  └──────────┘         └──────────┘          └──────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Why Use MotherDuck?

**Benefits:**
- **Persistence**: Cloud storage for your databases
- **Collaboration**: Share databases with teams
- **Scalability**: Handle datasets larger than local memory
- **Accessibility**: Access data from anywhere
- **Integration**: Connect with BI tools and other services
- **Cost-Effective**: Pay only for what you use
- **DuckDB Native**: Same SQL and functionality as local DuckDB

**Use Cases:**
- Team collaboration on data projects
- Storing and sharing large datasets
- Data warehousing for small to medium teams
- Quick prototyping with cloud data
- Educational and training environments
- Data science and ML workflows

## 🚀 Step-by-Step Instructions

### Step 1: Set Up MotherDuck Account

1. Sign up for MotherDuck at https://motherduck.com
2. Choose the free tier for learning
3. Create your first database through the web UI
4. Note your MotherDuck service token

### Step 2: Connect to MotherDuck via CLI

Connect to MotherDuck using the DuckDB CLI:

```bash
# Set your MotherDuck token as environment variable
export MOTHERDUCK_TOKEN='your_token_here'

# Connect to MotherDuck
duckdb md:

# Or connect to a specific database
duckdb md:my_database

# List available databases
.databases

# Switch between databases
.open md:another_database
```

### Step 3: Token-Based Authentication

Use token authentication programmatically:

```python
import duckdb
import os

# Set token as environment variable
os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

# Connect to MotherDuck
con = duckdb.connect('md:my_database')

# Test connection
result = con.execute("SELECT current_database()").fetchone()
print(f"Connected to: {result[0]}")

# List tables
tables = con.execute("SHOW TABLES").fetchall()
print(f"Tables: {tables}")
```

### Step 4: Upload Databases to MotherDuck

Upload your local database to MotherDuck:

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

# Connect to local database
local_con = duckdb.connect('data/duckdb_practice.db')

# Export to MotherDuck
local_con.execute("ATTACH 'md:my_cloud_db' AS cloud_db (TYPE motherduck)")

# Copy data to cloud
local_con.execute("""
    CREATE TABLE cloud_db.customers AS 
    SELECT * FROM sample_customers
""")

local_con.execute("""
    CREATE TABLE cloud_db.products AS 
    SELECT * FROM sample_products
""")

print("Database uploaded to MotherDuck")
```

### Step 5: Create Databases in MotherDuck

Create databases directly in the cloud:

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

# Connect to MotherDuck (creates database if it doesn't exist)
con = duckdb.connect('md:new_database')

# Create tables directly in cloud
con.execute("""
    CREATE TABLE cloud_sales AS
    SELECT 
        (random() * 1000)::int as customer_id,
        (random() * 100)::int as product_id,
        random() * 500 as amount,
        '2023-01-01'::date + (random() * 365)::int as sale_date
    FROM range(10000)
""")

print("Database created in MotherDuck")
```

### Step 6: Share Databases

Share databases with collaborators:

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

con = duckdb.connect('md:my_database')

# Grant permissions (if supported by your plan)
# Note: Sharing features depend on your MotherDuck plan

# Alternative: Export and share
con.execute("EXPORT DATABASE 'data/shared_backup' (FORMAT PARQUET)")

# Share the backup files or database connection details
print("Database ready for sharing")
```

### Step 7: Manage S3 Secrets and Load Data from S3

Configure S3 access and load data:

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

con = duckdb.connect('md:my_database')

# Set S3 credentials
con.execute("""
    CREATE SECRET s3_secret (
        TYPE S3,
        KEY_ID 'your_access_key',
        SECRET 'your_secret_key',
        REGION 'us-east-1'
    )
""")

# Load data from S3
con.execute("""
    CREATE TABLE s3_data AS
    SELECT * FROM read_parquet('s3://your-bucket/data/*.parquet')
""")

print("Data loaded from S3")
```

### Step 8: Optimize Data Ingestion

Optimize data loading into MotherDuck:

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

con = duckdb.connect('md:my_database')

# Batch insertion for better performance
def batch_insert(data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        con.register('temp_batch', batch)
        con.execute("INSERT INTO target_table SELECT * FROM temp_batch")
        con.execute("DROP TABLE temp_batch")

# Use COPY for bulk loading
con.execute("""
    COPY target_table FROM 'local_data.csv' (
        FORMAT CSV,
        DELIMITER ',',
        HEADER
    )
""")

# Configure for optimal performance
con.execute("SET enable_progress_bar=true")
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=4")

print("Optimized data ingestion configured")
```

### Step 9: Query Data with AI

Use AI assistance for querying (if available):

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

con = duckdb.connect('md:my_database')

# Note: AI query features depend on MotherDuck plan
# Example of how AI-assisted querying might work:

# Traditional query
result = con.execute("""
    SELECT customer_id, SUM(amount) as total
    FROM sales
    GROUP BY customer_id
    ORDER BY total DESC
    LIMIT 10
""").fetchdf()

print("Query results:")
print(result)

# AI-assisted query (if available in your plan)
# This would typically be done through the MotherDuck UI
```

### Step 10: Explore Integrations

Explore MotherDuck integrations:

```python
import duckdb
import os

os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'

con = duckdb.connect('md:my_database')

# Integration with popular tools

# 1. BI Tools (via standard SQL connections)
# MotherDuck can be connected from:
# - Metabase
# - Superset
# - Grafana
# - Tableau (via ODBC)

# 2. Data pipelines
# - Airflow
# - Dagster
# - Prefect

# 3. Notebooks
# - Jupyter
# - Google Colab
# - Deepnote

# 4. Programming languages
# - Python (duckdb package)
# - R (duckdb package)
# - Java (JDBC driver)

print("MotherDuck supports integration with many tools")
print("Check MotherDuck documentation for specific setup instructions")
```

## 💻 Hands-On Exercises

### Exercise 1: MotherDuck Setup and Connection

Set up your MotherDuck environment:

```python
import duckdb
import os

# Set up your MotherDuck connection
# Your code here to:
# 1. Set environment variables
# 2. Connect to MotherDuck
# 3. Test the connection
# 4. Create a test database
```

### Exercise 2: Data Upload and Management

Practice uploading and managing data:

```python
import duckdb
import os

# Your code here to:
# 1. Upload local database to MotherDuck
# 2. Create tables in MotherDuck
# 3. Copy data between local and cloud
# 4. Verify data integrity
```

### Exercise 3: Cloud Data Analysis

Perform analysis on cloud data:

```python
import duckdb
import os

# Your code here to:
# 1. Connect to MotherDuck database
# 2. Perform complex queries
# 3. Create views and materialized views
# 4. Export results
```

### Exercise 4: S3 Integration

Practice S3 data loading:

```python
import duckdb
import os

# Your code here to:
# 1. Configure S3 credentials
# 2. Load data from S3 bucket
# 3. Query S3 data directly
# 4. Optimize S3 queries
```

### Exercise 5: Performance Optimization

Optimize MotherDuck performance:

```python
import duckdb
import os

# Your code here to:
# 1. Test different batch sizes for data loading
# 2. Configure memory and thread settings
# 3. Measure query performance
# 4. Implement caching strategies
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Have a working MotherDuck account
2. ✅ Be able to connect to MotherDuck via CLI and Python
3. ✅ Understand token-based authentication
4. ✅ Be able to upload and manage databases in the cloud
5. ✅ Know how to share databases with collaborators
6. ✅ Be able to configure S3 access and load data
7. ✅ Understand performance optimization techniques
8. ✅ Be familiar with MotherDuck integrations

## 🔍 Verification

Verify your MotherDuck setup:

```python
import duckdb
import os

print("=== MotherDuck Verification ===")

# Test 1: Connection
if 'MOTHERDUCK_TOKEN' in os.environ:
    print("✓ MotherDuck token configured")
else:
    print("✗ MotherDuck token not set")

# Test 2: Database connection
try:
    con = duckdb.connect('md:')
    result = con.execute("SELECT current_database()").fetchone()
    print(f"✓ Connected to MotherDuck: {result[0]}")
    con.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")

# Test 3: Database operations
try:
    con = duckdb.connect('md:test_verification')
    con.execute("CREATE TABLE test AS SELECT * FROM range(10)")
    count = con.execute("SELECT COUNT(*) FROM test").fetchone()[0]
    print(f"✓ Database operations: {count} rows")
    con.close()
except Exception as e:
    print(f"✗ Database operations failed: {e}")

print("=== Verification Complete ===")
```

## 🆘 Troubleshooting

### Issue: Connection fails

**Solution**: Verify token and network connection:
```python
import os
print(f"Token set: {bool(os.environ.get('MOTHERDUCK_TOKEN'))}")
print(f"Token length: {len(os.environ.get('MOTHERDUCK_TOKEN', ''))}")
```

### Issue: S3 access denied

**Solution**: Check credentials and permissions:
```python
# Verify S3 secret configuration
con.execute("SELECT * FROM duckdb_secrets()")
```

### Issue: Slow data loading

**Solution**: Optimize batch size and configuration:
```python
con.execute("SET memory_limit='4GB'")
con.execute("SET threads=8")
# Use smaller batches for better performance
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 8**: Building Data Pipelines
2. **Explore MotherDuck UI**: Use the web interface for database management
3. **Practice sharing**: Share a database with a colleague
4. **Integrate with tools**: Connect MotherDuck to your favorite BI tool

---

**You now have the skills to use DuckDB in the cloud with MotherDuck for scalable, collaborative data analytics!**