# Lakehouse Architecture

This document explains lakehouse architecture concepts and how DuckDB fits into modern data lakehouse implementations.

## 🏗️ What is a Lakehouse?

A lakehouse is a modern data architecture that combines the best elements of data lakes and data warehouses:

### Data Lake Characteristics
- **Low-cost storage**: Object storage (S3, Azure Blob, GCS)
- **Flexible schema**: Schema-on-read capabilities
- **Open formats**: Parquet, Avro, ORC, Delta, Iceberg
- **Scalability**: Handle petabytes of data
- **Flexibility**: Support diverse data types

### Data Warehouse Characteristics  
- **ACID transactions**: Data integrity and consistency
- **Schema enforcement**: Data quality and governance
- **Performance**: Optimized for analytics workloads
- **BI support**: Direct integration with BI tools
- **Concurrency**: Support for multiple users

### Lakehouse Benefits
- **Cost-effective**: Low-cost storage with warehouse performance
- **Open formats**: No vendor lock-in
- **Unified platform**: Both ML and BI workloads
- **Reliability**: ACID transactions and data governance
- **Flexibility**: Support for diverse data types and workloads

## 🎯 Lakehouse Architecture Layers

### Layer 1: Bronze Layer (Raw Data)

**Purpose**: Ingest raw data without transformation

**Characteristics**:
- Append-only, immutable data
- Original format preservation
- Minimal validation
- Low cost storage
- Data lineage tracking

**DuckDB Role**:
- Query raw data efficiently
- Initial data validation
- Quick data exploration
- Format conversion

```python
# Bronze layer example
con.execute("""
    COPY raw_events TO 's3://lakehouse/bronze/events/' 
    (FORMAT PARQUET, COMPRESSION 'snappy')
""")
```

### Layer 2: Silver Layer (Cleaned Data)

**Purpose**: Clean, validate, and standardize data

**Characteristics**:
- Data validation and quality checks
- Schema standardization
- Deduplication
- Data enrichment
- Partitioning for performance

**DuckDB Role**:
- Data transformation and cleaning
- Complex validation logic
- Schema evolution
- Performance optimization

```python
# Silver layer example
con.execute("""
    COPY (
        SELECT 
            event_id,
            customer_id,
            event_timestamp,
            event_type,
            -- Data cleaning and validation
            CASE 
                WHEN event_timestamp > CURRENT_TIMESTAMP THEN NULL
                ELSE event_timestamp
            END as validated_timestamp
        FROM bronze_events
    ) TO 's3://lakehouse/silver/events/' 
    (FORMAT PARQUET, PARTITION_BY (event_type, DATE_TRUNC('day', event_timestamp)))
""")
```

### Layer 3: Gold Layer (Business-Ready Data)

**Purpose**: Aggregated, business-ready data for analytics

**Characteristics**:
- Pre-computed aggregations
- Business metrics
- Optimized for query performance
- Star/snowflake schemas
- BI tool integration

**DuckDB Role**:
- Fast analytical queries
- Complex aggregations
- BI integration
- Real-time dashboards

```python
# Gold layer example
con.execute("""
    COPY (
        SELECT 
            DATE_TRUNC('day', event_timestamp) as day,
            event_type,
            COUNT(*) as event_count,
            COUNT(DISTINCT customer_id) as unique_customers,
            AVG(session_duration) as avg_session_duration
        FROM silver_events
        GROUP BY day, event_type
    ) TO 's3://lakehouse/gold/daily_metrics/' 
    (FORMAT PARQUET, COMPRESSION 'zstd')
""")
```

## 🔧 DuckDB in Lakehouse Architecture

### Query Engine Role

DuckDB serves as a high-performance query engine in the lakehouse:

**Advantages**:
- **Fast execution**: Vectorized query execution
- **Zero-copy integration**: Direct Parquet/Arrow access
- **SQL compatibility**: Standard SQL with extensions
- **Embedded mode**: No separate server needed
- **Cost-effective**: Efficient resource utilization

**Use Cases**:
- Ad-hoc data exploration
- Data validation and quality checks
- ETL pipeline processing
- BI backend for dashboards
- Machine learning data preparation

### Integration Patterns

#### Pattern 1: Direct File Querying

Query data lake files directly without ingestion:

```python
# Query S3 data directly
con.execute("""
    SELECT * FROM 's3://bucket/lakehouse/silver/events/*.parquet'
    WHERE event_date >= '2024-01-01'
""")
```

#### Pattern 2: Local Caching

Cache frequently accessed data locally:

```python
# Cache remote data locally
con.execute("""
    CREATE OR REPLACE TABLE cached_events AS
    SELECT * FROM 's3://bucket/lakehouse/gold/daily_metrics/*.parquet'
""")

# Query cached data
con.execute("SELECT * FROM cached_events WHERE day = '2024-01-01'")
```

#### Pattern 3: Hybrid Processing

Combine local and remote data processing:

```python
# Join local and remote data
con.execute("""
    SELECT 
        l.customer_id,
        l.local_data,
        r.remote_data
    FROM local_table l
    JOIN 's3://bucket/remote_data.parquet' r ON l.id = r.id
""")
```

### Lakehouse Table Formats

#### Apache Iceberg Integration

DuckDB can query Iceberg tables:

```python
# Query Iceberg table
con.execute("""
    SELECT * FROM 's3://bucket/iceberg_table/' 
    WHERE event_timestamp >= '2024-01-01'
""")
```

#### Delta Lake Integration

Read Delta Lake format (via extensions):

```python
# Load Delta Lake extension
con.execute("INSTALL delta")
con.execute("LOAD delta")

# Query Delta table
con.execute("""
    SELECT * FROM delta_scan('s3://bucket/delta_table/')
""")
```

## 🚀 Lakehouse Implementation Patterns

### Pattern 1: Medallion Architecture

Implement the bronze-silver-gold layer pattern:

```python
class LakehouseMedallion:
    def __init__(self, connection):
        self.con = connection
    
    def bronze_to_silver(self, bronze_path, silver_path):
        """Transform bronze to silver layer"""
        self.con.execute(f"""
            COPY (
                SELECT 
                    -- Data cleaning and validation
                    id,
                    clean_string(name) as name,
                    validate_timestamp(timestamp) as timestamp,
                    standardize_category(category) as category
                FROM '{bronze_path}'
            ) TO '{silver_path}' (FORMAT PARQUET)
        """)
    
    def silver_to_gold(self, silver_path, gold_path):
        """Transform silver to gold layer"""
        self.con.execute(f"""
            COPY (
                SELECT 
                    -- Business aggregations
                    DATE_TRUNC('day', timestamp) as day,
                    category,
                    COUNT(*) as record_count,
                    AVG(value) as avg_value,
                    SUM(value) as total_value
                FROM '{silver_path}'
                GROUP BY day, category
            ) TO '{gold_path}' (FORMAT PARQUET)
        """)
```

### Pattern 2: Data Skipping

Implement partitioning and data skipping:

```python
# Partition data by date
con.execute("""
    COPY (
        SELECT * FROM events
    ) TO 's3://lakehouse/silver/events/' 
    (FORMAT PARQUET, PARTITION_BY (DATE_TRUNC('day', event_timestamp), event_type))
""")

# Query with partition pruning
con.execute("""
    SELECT * FROM 's3://lakehouse/silver/events/'
    WHERE event_timestamp >= '2024-01-01' AND event_type = 'click'
""")
```

### Pattern 3: Time Travel

Implement versioning and time travel:

```python
# Query specific version
con.execute("""
    SELECT * FROM 's3://lakehouse/silver/events/version=20240101'
""")

# Compare versions
con.execute("""
    SELECT 
        current.*,
        previous.*
    FROM 's3://lakehouse/silver/events/version=current' current
    FULL OUTER JOIN 's3://lakehouse/silver/events/version=20240101' previous
    ON current.id = previous.id
""")
```

## 📊 Lakehouse vs Traditional Architectures

### Data Warehouse Comparison

| Feature | Data Warehouse | Lakehouse |
|---------|----------------|-----------|
| Storage Cost | High (proprietary) | Low (object storage) |
| Data Formats | Proprietary | Open (Parquet, etc.) |
| Schema Flexibility | Rigid | Flexible |
| ML Support | Limited | Native |
| ACID Transactions | Yes | Yes |
| Query Performance | Optimized | Optimized |
| Vendor Lock-in | High | Low |

### Data Lake Comparison

| Feature | Data Lake | Lakehouse |
|---------|------------|-----------|
| ACID Transactions | No | Yes |
| Schema Enforcement | None | Strong |
| Query Performance | Variable | Optimized |
| BI Support | Limited | Native |
| Data Quality | Manual | Automated |
| Concurrency | Limited | High |

## 🎯 DuckDB Lakehouse Best Practices

### 1. File Format Optimization

**Use Parquet with appropriate compression**:
```python
# Use Snappy for balanced performance
con.execute("COPY table TO 'path/' (FORMAT PARQUET, COMPRESSION 'snappy')")

# Use ZSTD for maximum compression
con.execute("COPY table TO 'path/' (FORMAT PARQUET, COMPRESSION 'zstd')")
```

### 2. Partitioning Strategy

**Partition by frequently filtered columns**:
```python
# Partition by date for time-series data
con.execute("""
    COPY table TO 'path/' 
    (FORMAT PARQUET, PARTITION_BY (DATE_TRUNC('day', event_date)))
""")

# Partition by category for categorical data
con.execute("""
    COPY table TO 'path/' 
    (FORMAT PARQUET, PARTITION_BY (category))
""")
```

### 3. Row Group Size Optimization

**Configure row group size based on data size**:
```python
# Larger row groups for large datasets
con.execute("""
    COPY table TO 'path/' 
    (FORMAT PARQUET, ROW_GROUP_SIZE 1000000)
""")
```

### 4. Column Pruning

**Select only needed columns**:
```python
# Good: Select specific columns
con.execute("SELECT col1, col2 FROM table")

# Avoid: SELECT *
con.execute("SELECT * FROM table")
```

### 5. Predicate Pushdown

**Filter data at the source**:
```python
# DuckDB pushes predicates to Parquet reader
con.execute("""
    SELECT * FROM 's3://path/data.parquet'
    WHERE date >= '2024-01-01' AND category = 'A'
""")
```

## 🔮 Advanced Lakehouse Patterns

### 1. Change Data Capture (CDC)

Implement CDC patterns with DuckDB:

```python
# Process CDC events
con.execute("""
    COPY (
        SELECT 
            event_id,
            operation_type,  -- INSERT, UPDATE, DELETE
            before_state,
            after_state,
            event_timestamp
        FROM cdc_stream
    ) TO 's3://lakehouse/bronze/cdc/' 
    (FORMAT PARQUET)
""")
```

### 2. Real-time Analytics

Combine DuckDB with streaming data:

```python
# Process streaming data in micro-batches
while True:
    # Read latest batch
    batch = read_streaming_batch()
    
    # Process with DuckDB
    con.register('stream_batch', batch)
    result = con.execute("""
        SELECT 
            window_start,
            window_end,
            COUNT(*) as event_count,
            AVG(value) as avg_value
        FROM stream_batch
        GROUP BY window_start, window_end
    """).df()
    
    # Store results
    store_analytics(result)
```

### 3. Machine Learning Integration

Direct ML pipeline integration:

```python
# Feature engineering with DuckDB
features = con.execute("""
    SELECT 
        customer_id,
        -- Feature engineering
        AVG(order_value) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date 
            ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
        ) as rolling_avg_order_value,
        COUNT(*) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date 
            RANGE BETWEEN INTERVAL 30 DAYS PRECEDING AND CURRENT ROW
        ) as 30_day_order_count
    FROM orders
""").df()

# Train ML model
model = train_model(features)

# Store predictions back to DuckDB
con.register('predictions', predictions_df)
con.execute("""
    COPY predictions TO 's3://lakehouse/gold/predictions/' 
    (FORMAT PARQUET)
""")
```

## 📈 Monitoring and Optimization

### Lakehouse Performance Monitoring

Monitor key metrics across layers:

```python
# Monitor layer performance
def monitor_lakehouse_performance():
    metrics = {
        'bronze': {
            'query_time': measure_query_time('bronze'),
            'data_size': get_layer_size('bronze'),
            'file_count': count_files('bronze')
        },
        'silver': {
            'query_time': measure_query_time('silver'),
            'data_size': get_layer_size('silver'),
            'file_count': count_files('silver')
        },
        'gold': {
            'query_time': measure_query_time('gold'),
            'data_size': get_layer_size('gold'),
            'file_count': count_files('gold')
        }
    }
    return metrics
```

### Cost Optimization

Optimize storage and compute costs:

```python
# Implement data lifecycle policies
def implement_lifecycle_policy():
    # Archive old bronze data
    con.execute("""
        COPY (
            SELECT * FROM bronze_events
            WHERE event_timestamp < CURRENT_DATE - INTERVAL '90 days'
        ) TO 's3://archive/bronze_events/' 
        (FORMAT PARQUET, COMPRESSION 'zstd')
    """)
    
    # Delete archived data from hot storage
    con.execute("""
        DELETE FROM bronze_events
        WHERE event_timestamp < CURRENT_DATE - INTERVAL '90 days'
    """)
```

## 🎯 Production Considerations

### Scalability

**Horizontal scaling with multiple DuckDB instances**:
```python
# Distribute queries across instances
instances = ['duckdb-1', 'duckdb-2', 'duckdb-3']

# Partition data across instances
for i, instance in enumerate(instances):
    query = f"""
        SELECT * FROM large_table
        WHERE hash(id) % {len(instances)} = {i}
    """
    execute_on_instance(instance, query)
```

### High Availability

**Implement high availability patterns**:
```python
# Read replicas for query load balancing
primary = 'duckdb-primary'
replicas = ['duckdb-replica-1', 'duckdb-replica-2']

# Write to primary
execute_on_instance(primary, write_query)

# Read from replicas
execute_on_instance(replicas[0], read_query)
```

### Disaster Recovery

**Implement comprehensive disaster recovery**:
```python
# Multi-region replication
regions = ['us-east-1', 'us-west-2', 'eu-west-1']

for region in regions:
    con.execute(f"""
        COPY table TO 's3://{region}/lakehouse/' 
        (FORMAT PARQUET)
    """)
```

---

**This lakehouse architecture guide provides the foundation for building modern, scalable data platforms with DuckDB!**