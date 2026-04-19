# Lab 7: Extensions & Advanced Features

## 🎯 Learning Objectives

- Master DuckDB extension ecosystem
- Use HTTP filesystem for remote data access
- Implement spatial data processing
- Work with advanced JSON operations
- Create custom functions and UDFs
- Explore lakehouse extension patterns

## 📋 Prerequisites

- Completed Lab 6: Performance Optimization
- Working DuckDB environment
- Sample database loaded
- Internet connection for remote data access

## ⏱️ Estimated Time

60-90 minutes

## 🎓 Conceptual Background

DuckDB's extension system enables advanced capabilities beyond core functionality. This lab covers:

**Extension Ecosystem**: Installing and managing DuckDB extensions
**HTTP Filesystem**: Accessing remote data via HTTP/HTTPS
**Spatial Extensions**: Geospatial data processing and analysis
**Advanced JSON**: Complex JSON querying and manipulation
**Custom Functions**: User-defined functions for specialized processing
**Lakehouse Extensions**: Extensions for modern data architectures

## 🚀 Step-by-Step Instructions

### Step 1: Extension Management

Learn to install, load, and manage DuckDB extensions.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Check available extensions
print("Available extensions:")
available_extensions = con.execute("SELECT * FROM duckdb_extensions()").fetchdf()
print(available_extensions)

# Install and load httpfs extension
print("\nInstalling httpfs extension...")
con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")
print("httpfs extension loaded")

# Verify extension is loaded
print("\nLoaded extensions:")
loaded_extensions = con.execute("""
    SELECT * FROM duckdb_extensions() 
    WHERE loaded = true
""").fetchdf()
print(loaded_extensions)

# Install parquet extension (if not already loaded)
print("\nInstalling parquet extension...")
con.execute("INSTALL parquet")
con.execute("LOAD parquet")
print("parquet extension loaded")

# Install json extension
print("\nInstalling json extension...")
con.execute("INSTALL json")
con.execute("LOAD json")
print("json extension loaded")

# Extension auto-loading
print("\nExtension auto-loading...")
con.execute("SET autoload_known_extensions=true")
print("Auto-load enabled for known extensions")
```

### Step 2: HTTP Filesystem Extension

Access and query remote data via HTTP/HTTPS.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Ensure httpfs is loaded
con.execute("LOAD httpfs")

# Query remote Parquet file
print("Querying remote data...")

# Example: Query a public dataset
try:
    # Query remote CSV file
    remote_csv = """
    SELECT * FROM read_csv_auto('https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv')
    LIMIT 5
    """
    result = con.execute(remote_csv).fetchdf()
    print("Remote CSV data:")
    print(result)
except Exception as e:
    print(f"Remote data access failed: {e}")
    print("Using local data instead")

# HTTP filesystem configuration
print("\nHTTP filesystem configuration...")

# Configure HTTP settings
con.execute("SET enable_http_metadata_cache=true")
con.execute("SET enable_http_file_cache=true")
print("HTTP caching enabled")

# Query remote data with caching
try:
    cached_query = """
    SELECT * FROM read_parquet('https://github.com/duckdb/duckdb-web/raw/main/data/tpch/parquet/1/lineitem.parquet')
    LIMIT 5
    """
    result = con.execute(cached_query).fetchdf()
    print("Remote Parquet with caching:")
    print(result)
except Exception as e:
    print(f"Remote Parquet access failed: {e}")

# HTTP authentication (if needed)
print("\nHTTP authentication configuration...")
# con.execute("SET s3_access_key_id='your_key'")
# con.execute("SET s3_secret_access_key='your_secret'")
# con.execute("SET s3_endpoint='s3.amazonaws.com'")
print("HTTP authentication configured (commented out)")

# S3-compatible storage
print("\nS3-compatible storage access...")
# Example for S3 or S3-compatible storage
# s3_query = """
# SELECT * FROM read_parquet('s3://bucket/file.parquet')
# """
# result = con.execute(s3_query).fetchdf()
print("S3 access configured (commented out)")
```

### Step 3: Spatial Extensions

Process and analyze geospatial data.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Install and load spatial extension
print("Installing spatial extension...")
try:
    con.execute("INSTALL spatial")
    con.execute("LOAD spatial")
    print("Spatial extension loaded")
except Exception as e:
    print(f"Spatial extension installation failed: {e}")
    print("Spatial features may not be available in this environment")

# Basic spatial operations
if 'spatial' in str(con.execute("SELECT * FROM duckdb_extensions()").fetchdf()['extension_name'].tolist()):
    print("\nSpatial operations...")
    
    # Create points
    result = con.execute("SELECT ST_AsText(ST_Point(1, 2))").fetchone()
    print(f"Create point: {result[0]}")
    
    # Calculate distance
    result = con.execute("""
        SELECT ST_Distance(
            ST_Point(0, 0),
            ST_Point(3, 4)
        )
    """).fetchone()
    print(f"Distance between points: {result[0]}")
    
    # Buffer operation
    result = con.execute("""
        SELECT ST_AsText(
            ST_Buffer(ST_Point(0, 0), 1.0)
        )
    """).fetchone()
    print(f"Buffer result: {result[0]}")
    
    # Create spatial table
    con.execute("""
        CREATE OR REPLACE TABLE locations (
            id INTEGER,
            name VARCHAR,
            geom GEOMETRY
        )
    """)
    
    # Insert spatial data
    con.execute("""
        INSERT INTO locations VALUES 
        (1, 'Origin', ST_Point(0, 0)),
        (2, 'Point A', ST_Point(3, 4)),
        (3, 'Point B', ST_Point(6, 8))
    """)
    
    # Spatial query
    result = con.execute("""
        SELECT name, ST_AsText(geom) as geometry
        FROM locations
    """).fetchdf()
    print("Spatial table data:")
    print(result)
    
    # Spatial join example
    result = con.execute("""
        SELECT 
            l1.name as from_location,
            l2.name as to_location,
            ST_Distance(l1.geom, l2.geom) as distance
        FROM locations l1
        CROSS JOIN locations l2
        WHERE l1.id < l2.id
    """).fetchdf()
    print("Spatial distances:")
    print(result)
else:
    print("Spatial operations not available in this environment")

# Simulate spatial operations with regular data
print("\nSimulated spatial operations...")

# Create location data with coordinates
con.execute("""
    CREATE OR REPLACE TABLE customer_locations AS
    SELECT 
        customer_id,
        first_name,
        city,
        -- Simulate coordinates (in real scenario, use actual lat/long)
        (CAST(ABS(customer_id) % 100) AS DOUBLE) / 10.0 as latitude,
        (CAST(ABS(customer_id) % 100) AS DOUBLE) / 10.0 + 5.0 as longitude
    FROM sample_customers
    LIMIT 100
""")

# Distance calculation (Haversine formula simulation)
result = con.execute("""
    SELECT 
        customer_id,
        first_name,
        city,
        latitude,
        longitude,
        -- Simple Euclidean distance for demonstration
        SQRT(POW(latitude - 5.0, 2) + POW(longitude - 10.0, 2)) as distance_from_reference
    FROM customer_locations
    ORDER BY distance_from_reference
    LIMIT 10
""").fetchdf()
print("Customer distance analysis:")
print(result)
```

### Step 4: Advanced JSON Operations

Work with complex JSON data structures.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Ensure json extension is loaded
con.execute("LOAD json")

# Create complex JSON data
print("Creating complex JSON data...")

complex_json = """
{
    "customer": {
        "id": 1001,
        "name": "John Doe",
        "contact": {
            "email": "john@example.com",
            "phone": "555-1234"
        },
        "preferences": {
            "newsletter": true,
            "notifications": ["email", "sms"],
            "categories": ["electronics", "books"]
        }
    },
    "orders": [
        {
            "order_id": 5001,
            "items": [
                {"product_id": 1, "quantity": 2, "price": 99.99},
                {"product_id": 2, "quantity": 1, "price": 49.99}
            ],
            "total": 249.97
        }
    ]
}
"""

# Query nested JSON
print("\nQuerying nested JSON...")

# Extract nested values
result = con.execute(f"""
    SELECT 
        customer->'name' as customer_name,
        customer->'contact'->>'email' as email,
        customer->'preferences'->>'newsletter' as newsletter
    FROM (SELECT '{complex_json}'::JSON as customer)
""").fetchdf()
print("Nested JSON extraction:")
print(result)

# JSON array operations
print("\nJSON array operations...")

# Extract array elements
result = con.execute(f"""
    SELECT 
        json_array_length(customer->'orders') as order_count,
        customer->'orders'->0->>'order_id' as first_order_id
    FROM (SELECT '{complex_json}'::JSON as customer)
""").fetchdf()
print("JSON array operations:")
print(result)

# JSON aggregation
print("\nJSON aggregation...")

# Create sample JSON data
con.execute("""
    CREATE OR REPLACE TABLE json_customers AS
    SELECT 
        customer_id,
        first_name,
        {
            'segment': segment,
            'loyalty_points': loyalty_points,
            'is_active': is_active,
            'metrics': {
                'orders': 0,
                'revenue': 0.0
            }
        }::JSON as customer_json
    FROM sample_customers
    LIMIT 10
""")

# Query JSON data
result = con.execute("""
    SELECT 
        customer_id,
        customer_json->>'segment' as segment,
        customer_json->'metrics'->>'orders' as orders
    FROM json_customers
""").fetchdf()
print("JSON table query:")
print(result)

# JSON aggregation functions
result = con.execute("""
    SELECT 
        customer_json->>'segment' as segment,
        COUNT(*) as customer_count,
        SUM(customer_json->'loyalty_points'::INTEGER) as total_loyalty
    FROM json_customers
    GROUP BY segment
""").fetchdf()
print("JSON aggregation:")
print(result)
```

### Step 5: Custom Functions (UDFs)

Create user-defined functions for specialized processing.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Create scalar UDF in Python
print("Creating custom functions...")

# Define a Python function
def loyalty_tier(loyalty_points):
    if loyalty_points > 5000:
        return 'Platinum'
    elif loyalty_points > 3000:
        return 'Gold'
    elif loyalty_points > 1000:
        return 'Silver'
    else:
        return 'Bronze'

# Register the function
con.create_function('loyalty_tier', loyalty_tier)

# Use the custom function
result = con.execute("""
    SELECT 
        customer_id,
        loyalty_points,
        loyalty_tier(loyalty_points) as tier
    FROM sample_customers
    LIMIT 10
""").fetchdf()
print("Custom function results:")
print(result)

# Create aggregate UDF
print("\nCreating aggregate custom function...")

def weighted_avg(values, weights):
    if sum(weights) == 0:
        return 0
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)

# Register aggregate function
con.create_aggregate_function('weighted_avg', weighted_avg)

# Use aggregate function
result = con.execute("""
    SELECT 
        segment,
        weighted_avg(loyalty_points, loyalty_points) as weighted_avg_loyalty
    FROM sample_customers
    GROUP BY segment
""").fetchdf()
print("Aggregate function results:")
print(result)

# SQL UDF
print("\nCreating SQL UDF...")

con.execute("""
    CREATE OR REPLACE FUNCTION revenue_category(total_amount)
    AS CASE 
        WHEN total_amount > 500 THEN 'High'
        WHEN total_amount > 200 THEN 'Medium'
        ELSE 'Low'
    END
""")

# Use SQL UDF
result = con.execute("""
    SELECT 
        order_id,
        total_amount,
        revenue_category(total_amount) as category
    FROM sample_orders
    LIMIT 10
""").fetchdf()
print("SQL UDF results:")
print(result)

# Complex UDF with multiple parameters
print("\nCreating complex UDF...")

def customer_score(loyalty_points, order_count, avg_order_value):
    # Calculate a composite customer score
    loyalty_score = min(loyalty_points / 1000, 10)
    frequency_score = min(order_count / 10, 10)
    value_score = min(avg_order_value / 100, 10)
    return (loyalty_score + frequency_score + value_score) / 3

con.create_function('customer_score', customer_score)

# Use complex UDF
result = con.execute("""
    SELECT 
        c.customer_id,
        c.loyalty_points,
        COUNT(o.order_id) as order_count,
        AVG(o.total_amount) as avg_order_value,
        customer_score(c.loyalty_points, COUNT(o.order_id), AVG(o.total_amount)) as customer_score
    FROM sample_customers c
    LEFT JOIN sample_orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.loyalty_points
    LIMIT 10
""").fetchdf()
print("Complex UDF results:")
print(result)
```

### Step 6: Lakehouse Extension Patterns

Apply extensions to lakehouse architecture patterns.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Extension-based lakehouse patterns
print("Lakehouse extension patterns...")

# HTTP filesystem for bronze layer (external data)
print("\nBronze layer with HTTP filesystem...")

# Simulate external data access
# In real scenario, this would access remote data lakes
con.execute("""
    CREATE OR REPLACE VIEW bronze_external_data AS
    SELECT 
        'remote_source' as source,
        customer_id,
        first_name,
        segment,
        CURRENT_TIMESTAMP as ingestion_time
    FROM sample_customers
    LIMIT 100
""")

result = con.execute("SELECT * FROM bronze_external_data LIMIT 5").fetchdf()
print("External bronze layer:")
print(result)

# JSON for semi-structured silver layer
print("\nSilver layer with JSON processing...")

con.execute("""
    CREATE OR REPLACE VIEW silver_enriched AS
    SELECT 
        c.customer_id,
        c.first_name,
        c.segment,
        {
            'loyalty_tier': loyalty_tier(c.loyalty_points),
            'order_summary': {
                'total_orders': COUNT(o.order_id),
                'total_revenue': SUM(o.total_amount)
            },
            'enrichment_timestamp': CURRENT_TIMESTAMP
        }::JSON as enrichment_data
    FROM sample_customers c
    LEFT JOIN sample_orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.segment
    LIMIT 10
""")

result = con.execute("SELECT * FROM silver_enriched").fetchdf()
print("Enriched silver layer:")
print(result)

# Custom functions for gold layer business logic
print("\nGold layer with custom functions...")

# Business logic function
def business_health_score(customer_segment, revenue_growth, customer_satisfaction):
    segment_multiplier = {'Premium': 1.5, 'Standard': 1.0, 'Basic': 0.8}
    base_score = (revenue_growth * 0.6 + customer_satisfaction * 0.4)
    return base_score * segment_multiplier.get(customer_segment, 1.0)

con.create_function('business_health_score', business_health_score)

con.execute("""
    CREATE OR REPLACE VIEW gold_metrics AS
    SELECT 
        segment,
        COUNT(*) as customer_count,
        AVG(loyalty_points) as avg_loyalty,
        business_health_score(segment, 0.5, 0.8) as health_score
    FROM sample_customers
    GROUP BY segment
""")

result = con.execute("SELECT * FROM gold_metrics").fetchdf()
print("Business metrics gold layer:")
print(result)

# Extension integration monitoring
print("\nExtension usage monitoring...")

extension_usage = con.execute("""
    SELECT 
        extension_name,
        loaded,
        installed
    FROM duckdb_extensions()
""").fetchdf()
print("Extension status:")
print(extension_usage)

# Performance impact analysis
print("\nExtension performance impact...")

import time

# Query without extensions
con.execute("UNLOAD httpfs")
con.execute("UNLOAD json")

start = time.time()
basic_query = "SELECT COUNT(*) FROM sample_customers"
con.execute(basic_query).fetchone()
basic_time = time.time() - start

# Query with extensions
con.execute("LOAD httpfs")
con.execute("LOAD json")

start = time.time()
con.execute(basic_query).fetchone()
extended_time = time.time() - start

print(f"Basic query time: {basic_time:.4f}s")
print(f"Extended query time: {extended_time:.4f}s")
print(f"Extension overhead: {(extended_time - basic_time) / basic_time:.2%}")
```

## 💻 Hands-On Exercises

### Exercise 1: Build Remote Data Pipeline

Create a pipeline using HTTP filesystem extension:

```python
# Your code here
# Access remote data sources
# Implement caching strategies
# Handle authentication
# Monitor remote access performance
# Build resilient data loading
```

### Exercise 2: Geospatial Analytics

Implement geospatial analysis with spatial extension:

```python
# Your code here
# Process location data
# Calculate distances and areas
# Perform spatial joins
# Create geographic visualizations
# Build location-based insights
```

### Exercise 3: Advanced JSON Processing

Build complex JSON data processing workflows:

```python
# Your code here
# Parse nested JSON structures
# Transform JSON to relational format
# Implement JSON validation
# Build JSON aggregation pipelines
# Handle schema evolution
```

### Exercise 4: Custom Function Library

Create a library of useful custom functions:

```python
# Your code here
# Implement business logic functions
# Create data validation functions
# Build transformation functions
# Document function usage
# Optimize function performance
```

### Exercise 5: Extension-Based Lakehouse

Design lakehouse architecture leveraging extensions:

```python
# Your code here
# Plan extension usage across layers
# Implement extension-based optimizations
# Monitor extension performance
# Handle extension dependencies
# Create extension fallback strategies
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Master DuckDB extension management
2. ✅ Use HTTP filesystem for remote data
3. ✅ Process spatial data effectively
4. ✅ Handle complex JSON operations
5. ✅ Create and use custom functions
6. ✅ Apply extensions to lakehouse patterns

## 🔍 Verification

Test your extension skills:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Test extension loading
con.execute("LOAD httpfs")
con.execute("LOAD json")
print("Extension loading test: PASSED")

# Test custom function
con.create_function('test_func', lambda x: x * 2)
result = con.execute("SELECT test_func(5)").fetchone()
print(f"Custom function test: {result[0]}")

# Test JSON operations
json_test = con.execute("SELECT '{\"test\": 1}'::JSON->>'test'").fetchone()
print(f"JSON test: {json_test[0]}")

print("✅ Extension and advanced features test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: Extension installation fails

**Solution**: Check internet connection and try alternative mirrors:
```python
# Use specific extension version
con.execute("INSTALL httpfs FROM 'https://nightly-extensions.duckdb.org'")

# Check extension availability
con.execute("SELECT * FROM duckdb_extensions()")
```

### Issue: HTTP access blocked

**Solution**: Configure proxy or use alternative access:
```python
# Configure proxy
con.execute("SET http_proxy='http://proxy.example.com:8080'")

# Use alternative data sources
# Download locally and query local files
```

### Issue: Custom function performance

**Solution**: Optimize function implementation:
```python
# Use vectorized operations when possible
# Avoid loops in favor of SQL operations
# Cache expensive computations
# Use appropriate data types
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 8**: Real-World Use Cases and Patterns
2. **Explore extensions**: Deep dive into specific extensions
3. **Build function library**: Create reusable custom functions
4. **Integrate with lakehouse**: Apply extensions to production

---

**You now have comprehensive DuckDB extension skills for advanced data processing!**