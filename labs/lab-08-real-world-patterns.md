# Lab 8: Real-World Use Cases and Patterns

## 🎯 Learning Objectives

- Implement ETL patterns for data processing
- Build data quality and validation frameworks
- Create slowly changing dimensions (SCD)
- Design batch and streaming patterns
- Implement data reconciliation and auditing
- Learn lakehouse production patterns

## 📋 Prerequisites

- Completed Lab 7: Extensions & Advanced Features
- Working DuckDB environment
- Sample database loaded
- Understanding of data engineering concepts

## ⏱️ Estimated Time

60-90 minutes

## 🎓 Conceptual Background

Real-world data engineering requires proven patterns and practices. This lab covers:

**ETL Patterns**: Extract, Transform, Load workflows
**Data Quality**: Validation, cleaning, and monitoring
**SCD Implementation**: Slowly Changing Dimensions for tracking changes
**Batch Processing**: Periodic data processing workflows
**Streaming Patterns**: Real-time data processing simulation
**Lakehouse Patterns**: Production-ready data architecture patterns

## 🚀 Step-by-Step Instructions

### Step 1: ETL Pipeline Implementation

Build a complete ETL pipeline with error handling and monitoring.

```python
import duckdb
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

con = duckdb.connect('data/duckdb_practice.db')

class ETL Pipeline:
    def __init__(self, connection):
        self.con = connection
        self.pipeline_start_time = datetime.now()
        self.metrics = {
            'extracted': 0,
            'transformed': 0,
            'loaded': 0,
            'errors': 0
        }
    
    def extract(self, query, source_name):
        """Extract data from source"""
        try:
            logger.info(f"Extracting from {source_name}")
            start_time = datetime.now()
            
            df = self.con.execute(query).fetchdf()
            extraction_time = (datetime.now() - start_time).total_seconds()
            
            self.metrics['extracted'] += len(df)
            logger.info(f"Extracted {len(df)} rows from {source_name} in {extraction_time:.2f}s")
            
            return df
        except Exception as e:
            logger.error(f"Extraction failed from {source_name}: {e}")
            self.metrics['errors'] += 1
            raise
    
    def transform(self, df, transformation_name, transform_func):
        """Transform data using provided function"""
        try:
            logger.info(f"Applying transformation: {transformation_name}")
            start_time = datetime.now()
            
            transformed_df = transform_func(df)
            transformation_time = (datetime.now() - start_time).total_seconds()
            
            self.metrics['transformed'] += len(transformed_df)
            logger.info(f"Transformed {len(transformed_df)} rows in {transformation_time:.2f}s")
            
            return transformed_df
        except Exception as e:
            logger.error(f"Transformation failed: {transformation_name}: {e}")
            self.metrics['errors'] += 1
            raise
    
    def load(self, df, table_name, mode='append'):
        """Load data into destination table"""
        try:
            logger.info(f"Loading {len(df)} rows into {table_name}")
            start_time = datetime.now()
            
            if mode == 'replace':
                self.con.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            self.con.register('temp_load', df)
            self.con.execute(f"""
                CREATE OR REPLACE TABLE {table_name} AS 
                SELECT * FROM temp_load
            """)
            
            load_time = (datetime.now() - start_time).total_seconds()
            self.metrics['loaded'] += len(df)
            logger.info(f"Loaded {len(df)} rows into {table_name} in {load_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Load failed for {table_name}: {e}")
            self.metrics['errors'] += 1
            raise
    
    def get_metrics(self):
        """Get pipeline metrics"""
        total_time = (datetime.now() - self.pipeline_start_time).total_seconds()
        return {
            **self.metrics,
            'total_time_seconds': total_time,
            'rows_per_second': self.metrics['loaded'] / total_time if total_time > 0 else 0
        }

# Example ETL pipeline
print("Running ETL pipeline...")

pipeline = ETL Pipeline(con)

# Extract
customers_df = pipeline.extract(
    "SELECT * FROM sample_customers LIMIT 1000",
    "sample_customers"
)

# Transform: Add calculated fields
def add_calculated_fields(df):
    df['registration_year'] = pd.to_datetime(df['registration_date']).dt.year
    df['loyalty_tier'] = pd.cut(df['loyalty_points'], 
                                 bins=[0, 1000, 3000, 5000, float('inf')],
                                 labels=['Bronze', 'Silver', 'Gold', 'Platinum'])
    return df

transformed_customers = pipeline.transform(
    customers_df,
    "add_calculated_fields",
    add_calculated_fields
)

# Load
pipeline.load(transformed_customers, 'etl_customers', mode='replace')

# Get metrics
metrics = pipeline.get_metrics()
print("Pipeline metrics:")
print(metrics)
```

### Step 2: Data Quality Framework

Implement comprehensive data quality checks and validation.

```python
import duckdb
import pandas as pd

con = duckdb.connect('data/duckdb_practice.db')

class DataQualityValidator:
    def __init__(self, connection):
        self.con = connection
        self.validation_results = []
    
    def validate_not_null(self, table, column):
        """Check for NULL values in column"""
        result = self.con.execute(f"""
            SELECT COUNT(*) FROM {table} WHERE {column} IS NULL
        """).fetchone()[0]
        
        passed = result == 0
        self.validation_results.append({
            'check': 'not_null',
            'table': table,
            'column': column,
            'passed': passed,
            'details': f'{result} NULL values found'
        })
        
        return passed
    
    def validate_uniqueness(self, table, column):
        """Check for duplicate values in column"""
        result = self.con.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT {column}) 
            FROM {table}
        """).fetchone()[0]
        
        passed = result == 0
        self.validation_results.append({
            'check': 'uniqueness',
            'table': table,
            'column': column,
            'passed': passed,
            'details': f'{result} duplicate values found'
        })
        
        return passed
    
    def validate_range(self, table, column, min_value, max_value):
        """Check if values are within range"""
        result = self.con.execute(f"""
            SELECT COUNT(*) FROM {table} 
            WHERE {column} < {min_value} OR {column} > {max_value}
        """).fetchone()[0]
        
        passed = result == 0
        self.validation_results.append({
            'check': 'range',
            'table': table,
            'column': column,
            'passed': passed,
            'details': f'{result} values outside range [{min_value}, {max_value}]'
        })
        
        return passed
    
    def validate_referential_integrity(self, child_table, child_column, parent_table, parent_column):
        """Check referential integrity between tables"""
        result = self.con.execute(f"""
            SELECT COUNT(*) FROM {child_table} c
            LEFT JOIN {parent_table} p ON c.{child_column} = p.{parent_column}
            WHERE p.{parent_column} IS NULL
        """).fetchone()[0]
        
        passed = result == 0
        self.validation_results.append({
            'check': 'referential_integrity',
            'child_table': child_table,
            'child_column': child_column,
            'parent_table': parent_table,
            'parent_column': parent_column,
            'passed': passed,
            'details': f'{result} orphaned records found'
        })
        
        return passed
    
    def validate_data_freshness(self, table, date_column, max_age_days):
        """Check if data is fresh enough"""
        result = self.con.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE {date_column} < CURRENT_DATE - INTERVAL '{max_age_days} days'
        """).fetchone()[0]
        
        passed = result == 0
        self.validation_results.append({
            'check': 'data_freshness',
            'table': table,
            'column': date_column,
            'passed': passed,
            'details': f'{result} records older than {max_age_days} days'
        })
        
        return passed
    
    def get_validation_report(self):
        """Generate validation report"""
        df = pd.DataFrame(self.validation_results)
        
        total_checks = len(df)
        passed_checks = len(df[df['passed'] == True])
        failed_checks = len(df[df['passed'] == False])
        
        report = {
            'summary': {
                'total_checks': total_checks,
                'passed': passed_checks,
                'failed': failed_checks,
                'success_rate': passed_checks / total_checks if total_checks > 0 else 0
            },
            'details': df
        }
        
        return report

# Run data quality validation
print("Running data quality validation...")

validator = DataQualityValidator(con)

# Validate sample_customers
validator.validate_not_null('sample_customers', 'customer_id')
validator.validate_uniqueness('sample_customers', 'customer_id')
validator.validate_range('sample_customers', 'loyalty_points', 0, 10000)
validator.validate_data_freshness('sample_customers', 'registration_date', 3650)

# Validate referential integrity
validator.validate_referential_integrity('sample_orders', 'customer_id', 'sample_customers', 'customer_id')
validator.validate_referential_integrity('sample_orders', 'product_id', 'sample_products', 'product_id')

# Get validation report
report = validator.get_validation_report()
print("Data Quality Validation Report:")
print(f"Total checks: {report['summary']['total_checks']}")
print(f"Passed: {report['summary']['passed']}")
print(f"Failed: {report['summary']['failed']}")
print(f"Success rate: {report['summary']['success_rate']:.2%}")
print("\nDetailed results:")
print(report['details'])
```

### Step 3: Slowly Changing Dimensions (SCD)

Implement SCD types for tracking dimensional changes.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# SCD Type 1: Overwrite existing records
print("Implementing SCD Type 1...")

con.execute("""
    CREATE OR REPLACE TABLE customers_scd1 AS
    SELECT 
        customer_id,
        first_name,
        last_name,
        segment,
        loyalty_points,
        CURRENT_TIMESTAMP as last_updated
    FROM sample_customers
    LIMIT 100
""")

# Simulate update
con.execute("""
    UPDATE customers_scd1
    SET segment = 'Premium',
        last_updated = CURRENT_TIMESTAMP
    WHERE customer_id = 1
""")

print("SCD Type 1 implemented (overwrite changes)")

# SCD Type 2: Track history with effective dates
print("\nImplementing SCD Type 2...")

con.execute("""
    CREATE OR REPLACE TABLE customers_scd2 (
        customer_id INTEGER,
        first_name VARCHAR,
        last_name VARCHAR,
        segment VARCHAR,
        loyalty_points INTEGER,
        effective_date DATE,
        end_date DATE,
        is_current BOOLEAN,
        last_updated TIMESTAMP
    )
""")

# Initial load
con.execute("""
    INSERT INTO customers_scd2
    SELECT 
        customer_id,
        first_name,
        last_name,
        segment,
        loyalty_points,
        registration_date as effective_date,
        '9999-12-31'::DATE as end_date,
        true as is_current,
        CURRENT_TIMESTAMP as last_updated
    FROM sample_customers
    LIMIT 100
""")

# Simulate SCD Type 2 update
con.execute("""
    UPDATE customers_scd2
    SET end_date = CURRENT_DATE,
        is_current = false,
        last_updated = CURRENT_TIMESTAMP
    WHERE customer_id = 1 AND is_current = true
""")

con.execute("""
    INSERT INTO customers_scd2
    SELECT 
        customer_id,
        first_name,
        last_name,
        'Premium' as segment,
        loyalty_points + 1000 as loyalty_points,
        CURRENT_DATE as effective_date,
        '9999-12-31'::DATE as end_date,
        true as is_current,
        CURRENT_TIMESTAMP as last_updated
    FROM customers_scd2
    WHERE customer_id = 1 AND is_current = false
""")

print("SCD Type 2 implemented (track history)")

# Query SCD Type 2 history
history = con.execute("""
    SELECT * FROM customers_scd2 
    WHERE customer_id = 1
    ORDER BY effective_date
""").fetchdf()
print("Customer history:")
print(history)

# SCD Type 2 with surrogate key
print("\nImplementing SCD Type 2 with surrogate key...")

con.execute("""
    CREATE OR REPLACE TABLE customers_scd2_sk (
        surrogate_key INTEGER PRIMARY KEY,
        customer_id INTEGER,
        first_name VARCHAR,
        last_name VARCHAR,
        segment VARCHAR,
        loyalty_points INTEGER,
        effective_date DATE,
        end_date DATE,
        is_current BOOLEAN
    )
""")

# Use sequence for surrogate key
con.execute("CREATE SEQUENCE IF NOT EXISTS customer_surrogate_key_seq")
con.execute("SET GLOBAL customer_surrogate_key_seq_nextval = 1")

# Initial load with surrogate keys
con.execute("""
    INSERT INTO customers_scd2_sk
    SELECT 
        nextval('customer_surrogate_key_seq') as surrogate_key,
        customer_id,
        first_name,
        last_name,
        segment,
        loyalty_points,
        registration_date as effective_date,
        '9999-12-31'::DATE as end_date,
        true as is_current
    FROM sample_customers
    LIMIT 100
""")

print("SCD Type 2 with surrogate key implemented")
```

### Step 4: Batch Processing Patterns

Implement batch processing workflows for periodic data processing.

```python
import duckdb
from datetime import datetime, timedelta

con = duckdb.connect('data/duckdb_practice.db')

class BatchProcessor:
    def __init__(self, connection):
        self.con = connection
        self.batch_start_time = datetime.now()
        self.batch_results = []
    
    def process_daily_partition(self, partition_date):
        """Process a single daily partition"""
        print(f"Processing partition: {partition_date}")
        
        start_time = datetime.now()
        
        try:
            # Extract data for the partition
            partition_data = self.con.execute(f"""
                SELECT 
                    order_id,
                    customer_id,
                    product_id,
                    order_date,
                    quantity,
                    unit_price,
                    total_amount,
                    status,
                    payment_method
                FROM sample_orders
                WHERE order_date = '{partition_date}'
            """).fetchdf()
            
            # Transform data
            partition_data['processing_date'] = datetime.now()
            partition_data['partition_date'] = partition_date
            
            # Load to partitioned table
            self.con.register('temp_partition', partition_data)
            self.con.execute(f"""
                INSERT INTO orders_partitioned
                SELECT * FROM temp_partition
            """)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'partition_date': partition_date,
                'status': 'success',
                'rows_processed': len(partition_data),
                'processing_time': processing_time
            }
            
            print(f"Partition {partition_date} processed successfully: {len(partition_data)} rows in {processing_time:.2f}s")
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            result = {
                'partition_date': partition_date,
                'status': 'failed',
                'error': str(e),
                'processing_time': processing_time
            }
            print(f"Partition {partition_date} failed: {e}")
        
        self.batch_results.append(result)
        return result
    
    def process_date_range(self, start_date, end_date):
        """Process a range of dates"""
        print(f"Processing date range: {start_date} to {end_date}")
        
        current_date = start_date
        while current_date <= end_date:
            self.process_daily_partition(current_date)
            current_date += timedelta(days=1)
        
        return self.get_batch_summary()
    
    def get_batch_summary(self):
        """Get batch processing summary"""
        total_time = (datetime.now() - self.batch_start_time).total_seconds()
        
        successful_partitions = [r for r in self.batch_results if r['status'] == 'success']
        failed_partitions = [r for r in self.batch_results if r['status'] == 'failed']
        
        total_rows = sum(r.get('rows_processed', 0) for r in successful_partitions)
        
        return {
            'total_partitions': len(self.batch_results),
            'successful': len(successful_partitions),
            'failed': len(failed_partitions),
            'total_rows_processed': total_rows,
            'total_time_seconds': total_time,
            'average_partition_time': total_time / len(self.batch_results) if self.batch_results else 0,
            'results': self.batch_results
        }

# Create partitioned table
con.execute("""
    CREATE OR REPLACE TABLE orders_partitioned (
        order_id INTEGER,
        customer_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        quantity INTEGER,
        unit_price DECIMAL(10,2),
        total_amount DECIMAL(10,2),
        status VARCHAR,
        payment_method VARCHAR,
        processing_date TIMESTAMP,
        partition_date DATE
    )
""")

# Run batch processor
print("Running batch processor...")

processor = BatchProcessor(con)

# Process a date range (using available data)
start_date = datetime(2022, 1, 1).date()
end_date = datetime(2022, 1, 7).date()

summary = processor.process_date_range(start_date, end_date)

print("\nBatch Processing Summary:")
print(f"Total partitions: {summary['total_partitions']}")
print(f"Successful: {summary['successful']}")
print(f"Failed: {summary['failed']}")
print(f"Total rows processed: {summary['total_rows_processed']}")
print(f"Total time: {summary['total_time_seconds']:.2f}s")
print(f"Average partition time: {summary['average_partition_time']:.2f}s")
```

### Step 5: Data Reconciliation and Auditing

Implement data reconciliation and audit trails.

```python
import duckdb
from datetime import datetime

con = duckdb.connect('data/duckdb_practice.db')

# Create audit trail table
con.execute("""
    CREATE OR REPLACE TABLE data_audit_log (
        audit_id INTEGER PRIMARY KEY,
        table_name VARCHAR,
        operation VARCHAR,
        record_count INTEGER,
        checksum VARCHAR,
        operation_timestamp TIMESTAMP,
        user_name VARCHAR,
        status VARCHAR
    )
""")

# Create checksum function
def calculate_table_checksum(table_name):
    """Calculate a simple checksum for table data"""
    result = con.execute(f"""
        SELECT MD5(
            STRING_AGG(
                customer_id || '|' || 
                first_name || '|' || 
                COALESCE(segment, '') || '|' || 
                COALESCE(loyalty_points::VARCHAR, ''),
                '|'
            )
        ) as checksum
        FROM {table_name}
    """).fetchone()
    return result[0] if result else None

# Data reconciliation
class DataReconciler:
    def __init__(self, connection):
        self.con = connection
        self.reconciliation_results = []
    
    def reconcile_counts(self, table1, table2, key_column):
        """Reconcile record counts between two tables"""
        count1 = self.con.execute(f"SELECT COUNT(*) FROM {table1}").fetchone()[0]
        count2 = self.con.execute(f"SELECT COUNT(*) FROM {table2}").fetchone()[0]
        
        matched = count1 == count2
        result = {
            'check_type': 'count_reconciliation',
            'table1': table1,
            'table2': table2,
            'count1': count1,
            'count2': count2,
            'matched': matched,
            'difference': abs(count1 - count2)
        }
        
        self.reconciliation_results.append(result)
        return result
    
    def reconcile_data(self, table1, table2, key_column):
        """Reconcile actual data between two tables"""
        # Find records in table1 but not in table2
        only_in_table1 = self.con.execute(f"""
            SELECT COUNT(*) FROM {table1} t1
            LEFT JOIN {table2} t2 ON t1.{key_column} = t2.{key_column}
            WHERE t2.{key_column} IS NULL
        """).fetchone()[0]
        
        # Find records in table2 but not in table1
        only_in_table2 = self.con.execute(f"""
            SELECT COUNT(*) FROM {table2} t2
            LEFT JOIN {table1} t1 ON t2.{key_column} = t1.{key_column}
            WHERE t1.{key_column} IS NULL
        """).fetchone()[0]
        
        matched = (only_in_table1 == 0) and (only_in_table2 == 0)
        
        result = {
            'check_type': 'data_reconciliation',
            'table1': table1,
            'table2': table2,
            'key_column': key_column,
            'only_in_table1': only_in_table1,
            'only_in_table2': only_in_table2,
            'matched': matched
        }
        
        self.reconciliation_results.append(result)
        return result
    
    def log_audit(self, table_name, operation, record_count, status, user_name='system'):
        """Log audit information"""
        checksum = calculate_table_checksum(table_name)
        
        audit_id = self.con.execute(f"""
            SELECT COALESCE(MAX(audit_id), 0) + 1 
            FROM data_audit_log
        """).fetchone()[0]
        
        self.con.execute("""
            INSERT INTO data_audit_log 
            (audit_id, table_name, operation, record_count, checksum, operation_timestamp, user_name, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [audit_id, table_name, operation, record_count, checksum, datetime.now(), user_name, status])
        
        return audit_id
    
    def get_reconciliation_report(self):
        """Generate reconciliation report"""
        import pandas as pd
        df = pd.DataFrame(self.reconciliation_results)
        return df

# Run data reconciliation
print("Running data reconciliation...")

reconciler = DataReconciler(con)

# Reconcile between original and processed tables
reconciler.reconcile_counts('sample_customers', 'etl_customers', 'customer_id')
reconciler.reconcile_data('sample_customers', 'etl_customers', 'customer_id')

# Log audit
reconciler.log_audit('sample_customers', 'read', 1000, 'success')

# Get reconciliation report
report = reconciler.get_reconciliation_report()
print("Reconciliation Report:")
print(report)
```

### Step 6: Lakehouse Production Patterns

Implement production-ready lakehouse patterns.

```python
import duckdb
from datetime import datetime

con = duckdb.connect('data/duckdb_practice.db')

# Lakehouse production architecture
print("Implementing lakehouse production patterns...")

# Bronze layer: Raw data ingestion with metadata
con.execute("""
    CREATE OR REPLACE TABLE bronze_orders_raw (
        order_data JSON,
        ingestion_timestamp TIMESTAMP,
        source_system VARCHAR,
        batch_id VARCHAR,
        record_hash VARCHAR
    )
""")

# Ingest raw data
con.execute("""
    INSERT INTO bronze_orders_raw
    SELECT 
        {
            'order_id': order_id,
            'customer_id': customer_id,
            'product_id': product_id,
            'order_date': order_date,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': total_amount,
            'status': status,
            'payment_method': payment_method
        }::JSON as order_data,
        CURRENT_TIMESTAMP as ingestion_timestamp,
        'sample_system' as source_system,
        'batch_20240101' as batch_id,
        MD5(order_id::VARCHAR || customer_id::VARCHAR || order_date::VARCHAR) as record_hash
    FROM sample_orders
    LIMIT 100
""")

# Silver layer: Validated and transformed data
con.execute("""
    CREATE OR REPLACE TABLE silver_orders_validated (
        order_id INTEGER,
        customer_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        quantity INTEGER,
        unit_price DECIMAL(10,2),
        total_amount DECIMAL(10,2),
        status VARCHAR,
        payment_method VARCHAR,
        validation_status VARCHAR,
        validation_timestamp TIMESTAMP,
        data_quality_score INTEGER
    )
""")

# Transform and validate
con.execute("""
    INSERT INTO silver_orders_validated
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
        'validated' as validation_status,
        CURRENT_TIMESTAMP as validation_timestamp,
        CASE 
            WHEN total_amount > 0 AND status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled') THEN 100
            ELSE 0
        END as data_quality_score
    FROM (
        SELECT 
            CAST(order_data->>'order_id' AS INTEGER) as order_id,
            CAST(order_data->>'customer_id' AS INTEGER) as customer_id,
            CAST(order_data->>'product_id' AS INTEGER) as product_id,
            CAST(order_data->>'order_date' AS DATE) as order_date,
            CAST(order_data->>'quantity' AS INTEGER) as quantity,
            CAST(order_data->>'unit_price' AS DECIMAL(10,2)) as unit_price,
            CAST(order_data->>'total_amount' AS DECIMAL(10,2)) as total_amount,
            order_data->>'status' as status,
            order_data->>'payment_method' as payment_method
        FROM bronze_orders_raw
    ) raw_extracted
""")

# Gold layer: Business-ready aggregates
con.execute("""
    CREATE OR REPLACE TABLE gold_daily_metrics (
        metric_date DATE,
        total_orders INTEGER,
        total_revenue DECIMAL(15,2),
        avg_order_value DECIMAL(10,2),
        unique_customers INTEGER,
        delivered_orders INTEGER,
        delivery_rate DECIMAL(5,2),
        metric_timestamp TIMESTAMP
    )
""")

# Aggregate to gold layer
con.execute("""
    INSERT INTO gold_daily_metrics
    SELECT 
        order_date as metric_date,
        COUNT(*) as total_orders,
        SUM(total_amount) as total_revenue,
        AVG(total_amount) as avg_order_value,
        COUNT(DISTINCT customer_id) as unique_customers,
        SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
        CAST(SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS DECIMAL) / COUNT(*) as delivery_rate,
        CURRENT_TIMESTAMP as metric_timestamp
    FROM silver_orders_validated
    WHERE data_quality_score = 100
    GROUP BY order_date
""")

# Lakehouse metadata
con.execute("""
    CREATE OR REPLACE TABLE lakehouse_metadata (
        layer_name VARCHAR,
        table_name VARCHAR,
        row_count INTEGER,
        last_updated TIMESTAMP,
        data_freshness_date DATE,
        quality_score INTEGER,
        retention_policy VARCHAR
    )
""")

# Update metadata
con.execute("""
    INSERT INTO lakehouse_metadata
    VALUES 
    ('bronze', 'bronze_orders_raw', (SELECT COUNT(*) FROM bronze_orders_raw), CURRENT_TIMESTAMP, CURRENT_DATE, 100, '1 year'),
    ('silver', 'silver_orders_validated', (SELECT COUNT(*) FROM silver_orders_validated), CURRENT_TIMESTAMP, CURRENT_DATE, 100, '2 years'),
    ('gold', 'gold_daily_metrics', (SELECT COUNT(*) FROM gold_daily_metrics), CURRENT_TIMESTAMP, CURRENT_DATE, 100, '5 years')
""")

# Query lakehouse status
lakehouse_status = con.execute("SELECT * FROM lakehouse_metadata").fetchdf()
print("Lakehouse Status:")
print(lakehouse_status)

print("Lakehouse production patterns implemented successfully!")
```

## 💻 Hands-On Exercises

### Exercise 1: Build Complete ETL Pipeline

Create a production-ready ETL pipeline:

```python
# Your code here
# Implement error handling
# Add retry logic
# Create monitoring
# Build alerting
# Document pipeline
```

### Exercise 2: Advanced Data Quality Rules

Implement comprehensive data quality framework:

```python
# Your code here
# Define business rules
# Implement custom validations
# Create quality dashboards
# Build alerting system
# Automate remediation
```

### Exercise 3: Multi-Type SCD Implementation

Implement all SCD types in a unified framework:

```python
# Your code here
# SCD Type 0, 1, 2, 3
# Choose appropriate type per dimension
# Implement type switching
# Build history queries
# Optimize performance
```

### Exercise 4: Streaming Pattern Simulation

Simulate real-time data processing patterns:

```python
# Your code here
# Implement windowing
# Handle late-arriving data
# Create watermarking
# Build state management
# Monitor streaming metrics
```

### Exercise 5: Lakehouse Governance Framework

Implement comprehensive lakehouse governance:

```python
# Your code here
# Data lineage tracking
# Access control
# Data catalog
# Metadata management
# Compliance reporting
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Build production-ready ETL pipelines
2. ✅ Implement comprehensive data quality frameworks
3. ✅ Handle slowly changing dimensions
4. ✅ Design batch processing workflows
5. ✅ Implement data reconciliation
6. ✅ Apply lakehouse production patterns

## 🔍 Verification

Test your real-world pattern skills:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Test ETL pipeline
etl_test = con.execute("SELECT COUNT(*) FROM etl_customers").fetchone()
print(f"ETL pipeline test: {etl_test[0]} rows")

# Test data quality
quality_test = con.execute("SELECT COUNT(*) FROM customers_scd2").fetchone()
print(f"SCD test: {quality_test[0]} rows")

# Test batch processing
batch_test = con.execute("SELECT COUNT(*) FROM orders_partitioned").fetchone()
print(f"Batch processing test: {batch_test[0]} rows")

# Test lakehouse layers
lakehouse_test = con.execute("SELECT COUNT(*) FROM lakehouse_metadata").fetchone()
print(f"Lakehouse metadata test: {lakehouse_test[0]} layers")

print("✅ Real-world patterns test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: ETL pipeline failures

**Solution**: Implement robust error handling and retry logic:
```python
# Add try-catch blocks
# Implement exponential backoff
# Create checkpoint mechanisms
# Log detailed error information
```

### Issue: Data quality validation too slow

**Solution**: Optimize validation queries:
```python
# Use sampling for large datasets
# Implement incremental validation
# Cache validation results
# Use parallel validation
```

### Issue: SCD performance degradation

**Solution**: Optimize SCD implementation:
```python
# Use appropriate indexes
# Implement partitioning
# Archive old history
-- Use surrogate keys efficiently
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 9**: Integration and Production Readiness
2. **Build production pipelines**: Apply patterns to real data
3. **Study data governance**: Deep dive into compliance and security
4. **Implement monitoring**: Set up production monitoring systems

---

**You now have comprehensive real-world data engineering skills for production lakehouse environments!**