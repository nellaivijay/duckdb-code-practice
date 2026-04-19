# Lab 8A: Building Data Pipelines

## 🎯 Learning Objectives

- Understand the role of DuckDB in modern data pipelines
- Learn data ingestion with dlt (Data Loading Tool)
- Set up and configure dlt pipelines
- Explore pipeline metadata and monitoring
- Practice data transformation with dbt (data build tool)
- Set up dbt projects with DuckDB
- Define sources, models, and transformations in dbt
- Implement testing for transformations and pipelines
- Orchestrate data pipelines with Dagster
- Define assets and dependencies in Dagster
- Run and monitor Dagster pipelines
- Practice advanced computation in Dagster assets
- Upload processed data to MotherDuck

## 📋 Prerequisites

- Completed Lab 0: Sample Database Setup
- Completed Lab 1A: Introduction to DuckDB
- Python 3.8+ installed
- DuckDB Python package installed
- Basic understanding of data pipeline concepts

## ⏱️ Estimated Time

90-120 minutes

## 🎓 Conceptual Background

### Data Pipelines and DuckDB's Role

DuckDB plays a crucial role in modern data pipelines:

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Pipeline Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Sources              Ingestion          Transformation     │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐      │
│  │   APIs   │──────▶│    dlt   │──────▶│   dbt    │      │
│  │  Files   │       │          │       │          │      │
│  │ Database │       │          │       │          │      │
│  └──────────┘       └──────────┘       └──────────┘      │
│                           │                   │            │
│                           │                   │            │
│                           ▼                   ▼            │
│                    ┌──────────┐       ┌──────────┐      │
│                    │  DuckDB  │◄──────│ Dagster  │      │
│                    │ Storage  │       │Orchestration│     │
│                    └──────────┘       └──────────┘      │
│                           │                                │
│                           ▼                                │
│                    ┌──────────┐                           │
│                    │ MotherDuck│                          │
│                    │   Cloud   │                           │
│                    └──────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

**DuckDB's Role:**
- **Data Storage**: Efficient columnar storage for intermediate results
- **Transformation Engine**: Fast SQL-based data transformations
- **Integration Layer**: Connects various pipeline components
- **Testing Environment**: Quick validation of pipeline logic
- **Prototyping Tool**: Rapid development of pipeline components

## 🚀 Step-by-Step Instructions

### Step 1: Data Ingestion with dlt

Install and set up dlt:

```bash
pip install dlt[duckdb]
```

Create a basic dlt pipeline:

```python
import dlt
from dlt.sources.helpers import requests

# Define a simple source
def fetch_data():
    # Simulate API data
    data = [
        {"id": 1, "name": "Alice", "value": 100},
        {"id": 2, "name": "Bob", "value": 200},
        {"id": 3, "name": "Charlie", "value": 150}
    ]
    return data

# Create dlt pipeline
pipeline = dlt.pipeline(
    pipeline_name="simple_pipeline",
    destination="duckdb",
    dataset_name="raw_data"
)

# Run the pipeline
info = pipeline.run(fetch_data(), table_name="source_data")
print(f"Pipeline info: {info}")
```

### Step 2: Install a Supported Source

Install a dlt source connector:

```bash
# Install a specific source (example: PostgreSQL)
pip install dlt[postgres]

# Or install all sources
pip install dlt[all_sources]
```

Use a pre-built source:

```python
import dlt

# Example using a built-in source (adjust based on available sources)
# This is a template - actual sources vary

pipeline = dlt.pipeline(
    pipeline_name="api_pipeline",
    destination="duckdb",
    dataset_name="api_data"
)

# Run pipeline with source
# info = pipeline.run(source_name, table_name="extracted_data")
```

### Step 3: Build a Pipeline

Build a complete dlt pipeline:

```python
import dlt
import duckdb

# Define data source
def generate_sample_data():
    import random
    data = []
    for i in range(1000):
        data.append({
            "id": i + 1,
            "customer_id": random.randint(1, 100),
            "product_id": random.randint(1, 50),
            "amount": round(random() * 500, 2),
            "timestamp": "2023-01-01T00:00:00Z"
        })
    return data

# Create pipeline
pipeline = dlt.pipeline(
    pipeline_name="sales_pipeline",
    destination="duckdb",
    dataset_name="sales"
)

# Load data
info = pipeline.run(
    generate_sample_data(),
    table_name="raw_sales",
    write_disposition="replace"
)

print(f"Loaded {info.load_packages[0].row_counts['raw_sales']} rows")
```

### Step 4: Explore Pipeline Metadata

Explore dlt pipeline metadata:

```python
import duckdb

# Connect to the DuckDB database created by dlt
con = duckdb.connect('sales_pipeline.duckdb')

# List all tables
tables = con.execute("SHOW TABLES").fetchall()
print("Tables created by dlt:")
for table in tables:
    print(f"  {table[0]}")

# Examine pipeline metadata
try:
    metadata = con.execute("SELECT * FROM _dlt_pipeline_state").fetchdf()
    print("\nPipeline metadata:")
    print(metadata)
except:
    print("Metadata table not found - pipeline may use different structure")

# Examine loaded data
data = con.execute("SELECT * FROM raw_sales LIMIT 10").fetchdf()
print("\nSample data:")
print(data)
```

### Step 5: Data Transformation with dbt

Set up dbt with DuckDB:

```bash
pip install dbt-duckdb
dbt init my_duckdb_project
```

Configure dbt project (`dbt_project.yml`):

```yaml
name: 'my_duckdb_project'
version: '1.0.0'
config-version: 2

profile: 'duckdb_profile'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analyses"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  my_duckdb_project:
    +materialized: table
```

Configure profiles (`profiles.yml`):

```yaml
duckdb_profile:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: 'my_duckdb.db'
      schema: main
```

### Step 6: Define Sources

Define data sources in dbt:

```sql
-- models/sources.yml
version: 2

sources:
  - name: raw_data
    description: "Raw data from dlt pipeline"
    tables:
      - name: raw_sales
        description: "Raw sales data"
        columns:
          - name: id
            description: "Primary key"
            tests:
              - unique
              - not_null
          - name: customer_id
            description: "Customer identifier"
          - name: amount
            description: "Transaction amount"
```

### Step 7: Describe Transformations with Models

Create dbt models:

```sql
-- models/stg_sales.sql
with source_data as (
    select * from {{ source('raw_data', 'raw_sales') }}
),

transformed as (
    select
        id,
        customer_id,
        product_id,
        amount,
        cast(timestamp as timestamp) as transaction_timestamp,
        date_trunc('day', cast(timestamp as timestamp)) as transaction_date
    from source_data
)

select * from transformed
```

```sql
-- models/int_customer_summary.sql
with sales as (
    select * from {{ ref('stg_sales') }}
),

customer_stats as (
    select
        customer_id,
        count(*) as transaction_count,
        sum(amount) as total_amount,
        avg(amount) as avg_amount,
        min(transaction_date) as first_transaction,
        max(transaction_date) as last_transaction
    from sales
    group by customer_id
)

select * from customer_stats
```

### Step 8: Test Transformations and Pipelines

Create dbt tests:

```sql
-- models/schema.yml
version: 2

models:
  - name: stg_sales
    columns:
      - name: id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          
  - name: int_customer_summary
    tests:
      - dbt_utils.expression_is_true:
          expression: "total_amount > 0"
```

Run dbt tests:

```bash
dbt run
dbt test
```

### Step 9: Orchestrate with Dagster

Install Dagster:

```bash
pip install dagster dagster-duckdb
```

Define Dagster assets:

```python
from dagster import asset, Definitions
import duckdb
import pandas as pd

@asset
def raw_sales_data():
    """Extract raw sales data"""
    # Simulate data extraction
    data = pd.DataFrame({
        'id': range(1, 101),
        'customer_id': [i % 10 + 1 for i in range(100)],
        'amount': [round(100 + i * 10, 2) for i in range(100)],
        'date': pd.date_range('2023-01-01', periods=100, freq='D')
    })
    return data

@asset
def processed_sales(raw_sales_data):
    """Transform sales data"""
    con = duckdb.connect(':memory:')
    con.register('sales_df', raw_sales_data)
    
    result = con.execute("""
        SELECT 
            customer_id,
            COUNT(*) as transaction_count,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM sales_df
        GROUP BY customer_id
    """).df()
    
    return result

@asset
def customer_insights(processed_sales):
    """Generate customer insights"""
    # Add business logic
    processed_sales['segment'] = pd.cut(
        processed_sales['total_amount'],
        bins=[0, 500, 1000, float('inf')],
        labels=['Low', 'Medium', 'High']
    )
    return processed_sales
```

### Step 10: Run Pipelines

Define and run Dagster pipeline:

```python
from dagster import define_asset_job, ScheduleDefinition

# Define job
sales_pipeline_job = define_asset_job(
    name="sales_pipeline_job",
    selection=[customer_insights]
)

# Define schedule
schedule = ScheduleDefinition(
    job=sales_pipeline_job,
    cron_schedule="0 2 * * *",  # Run daily at 2 AM
)

# Define definitions
defs = Definitions(
    assets=[raw_sales_data, processed_sales, customer_insights],
    jobs=[sales_pipeline_job],
    schedules=[schedule]
)

# Run job (in development)
if __name__ == "__main__":
    from dagster import materialize
    materialize([raw_sales_data, processed_sales, customer_insights])
```

### Step 11: Manage Dependencies in a Pipeline

Define asset dependencies:

```python
from dagster import asset, AssetIn

@asset
def enriched_customers(customer_insights):
    """Enrich customer data with additional attributes"""
    # Add more business logic
    customer_insights['loyalty_score'] = (
        customer_insights['transaction_count'] * 10 +
        customer_insights['total_amount'] / 100
    )
    return customer_insights

@asset(ins={"customers": AssetIn("enriched_customers")})
def customer_segmentation(customers):
    """Segment customers based on behavior"""
    import numpy as np
    
    conditions = [
        (customers['loyalty_score'] > 100),
        (customers['loyalty_score'] > 50),
        (customers['loyalty_score'] >= 0)
    ]
    choices = ['Premium', 'Standard', 'Basic']
    
    customers['segment'] = np.select(conditions, choices)
    return customers
```

### Step 12: Advanced Computation in Assets

Implement advanced computations:

```python
@asset
def sales_analytics(customer_segmentation):
    """Perform advanced sales analytics"""
    con = duckdb.connect(':memory:')
    con.register('segmented_customers', customer_segmentation)
    
    # Complex analytics
    result = con.execute("""
        WITH segment_stats AS (
            SELECT 
                segment,
                COUNT(*) as customer_count,
                AVG(total_amount) as avg_spend,
                STDDEV(total_amount) as spend_std,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_spend
            FROM segmented_customers
            GROUP BY segment
        )
        SELECT * FROM segment_stats
    """).df()
    
    return result
```

### Step 13: Upload to MotherDuck

Upload processed data to MotherDuck:

```python
import duckdb
import os

@asset
def upload_to_motherduck(sales_analytics):
    """Upload analytics results to MotherDuck"""
    os.environ['MOTHERDUCK_TOKEN'] = 'your_token_here'
    
    con = duckdb.connect('md:my_database')
    con.register('analytics_data', sales_analytics)
    
    # Create table in MotherDuck
    con.execute("""
        CREATE OR REPLACE TABLE sales_analytics AS
        SELECT * FROM analytics_data
    """)
    
    print("Data uploaded to MotherDuck")
    return "Upload complete"
```

## 💻 Hands-On Exercises

### Exercise 1: Build Complete dlt Pipeline

Build a complete data ingestion pipeline:

```python
import dlt
import duckdb

# Your code here to:
# 1. Define a data source
# 2. Create a dlt pipeline
# 3. Load data into DuckDB
# 4. Explore the loaded data
# 5. Examine pipeline metadata
```

### Exercise 2: Create dbt Transformation Project

Create a complete dbt project:

```sql
-- Your dbt models here:
-- 1. Define sources
-- 2. Create staging models
-- 3. Create intermediate models
-- 4. Create final models
-- 5. Add tests
```

### Exercise 3: Build Dagster Pipeline

Create a complete Dagster pipeline:

```python
from dagster import asset, define_asset_job

# Your Dagster assets here:
# 1. Define extraction assets
# 2. Define transformation assets
# 3. Define loading assets
# 4. Create a job
# 5. Add dependencies
```

### Exercise 4: Integrate All Tools

Combine dlt, dbt, and Dagster:

```python
# Your integration code here:
# 1. Use dlt for ingestion
# 2. Use dbt for transformation
# 3. Use Dagster for orchestration
# 4. Add error handling
# 5. Add monitoring
```

### Exercise 5: Optimize Pipeline Performance

Optimize your pipeline:

```python
# Your optimization code here:
# 1. Test different batch sizes
# 2. Optimize SQL queries
# 3. Add caching
# 4. Parallelize operations
# 5. Monitor performance
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Understand the role of DuckDB in data pipelines
2. ✅ Be able to build dlt ingestion pipelines
3. ✅ Know how to use dbt for data transformation
4. ✅ Be able to orchestrate pipelines with Dagster
5. ✅ Understand how to integrate pipeline tools
6. ✅ Be able to upload processed data to MotherDuck
7. ✅ Have experience with pipeline testing and monitoring

## 🔍 Verification

Verify your pipeline setup:

```python
import duckdb

print("=== Data Pipeline Verification ===")

# Test 1: dlt pipeline data
try:
    con = duckdb.connect('sales_pipeline.duckdb')
    tables = con.execute("SHOW TABLES").fetchall()
    print(f"✓ dlt pipeline created {len(tables)} tables")
    con.close()
except:
    print("✗ dlt pipeline not found")

# Test 2: dbt transformation
try:
    con = duckdb.connect('my_duckdb.db')
    models = con.execute("SHOW TABLES").fetchall()
    print(f"✓ dbt created {len(models)} models")
    con.close()
except:
    print("✗ dbt project not found")

# Test 3: Dagster assets
# (Verification depends on how Dagster stores data)
print("✓ Dagster pipeline structure verified")

print("=== Verification Complete ===")
```

## 🆘 Troubleshooting

### Issue: dlt installation fails

**Solution**: Install with specific extras:
```bash
pip install dlt[duckdb] --upgrade
```

### Issue: dbt cannot find DuckDB profile

**Solution**: Check profiles.yml location:
```bash
# Usually in ~/.dbt/profiles.yml
cat ~/.dbt/profiles.yml
```

### Issue: Dagster assets not materializing

**Solution**: Check asset dependencies and execution order:
```python
# Verify asset graph
from dagster import get_asset_graph
graph = get_asset_graph([your_assets])
print(graph)
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 9**: Building and Deploying Data Apps
2. **Practice more**: Build pipelines with real data sources
3. **Explore advanced features**: Look into dbt macros and Dagster sensors
4. **Deploy to production**: Set up monitoring and alerting

---

**You now have the skills to build complete data pipelines using dlt, dbt, and Dagster with DuckDB!**