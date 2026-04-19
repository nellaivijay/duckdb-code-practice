# Sample Database Guide

Complete schema and usage documentation for the DuckDB Code Practice sample database.

## 📊 Database Overview

The sample database provides realistic business data for hands-on learning DuckDB and lakehouse concepts. It includes five related tables that simulate an e-commerce business scenario.

## 🗄️ Database Schema

### Table Relationships

```
sample_customers (1,000 records)
    ↓
sample_orders (5,000 records)
    ↓
sample_transactions (10,000 records)

sample_products (200 records)
    ↓
sample_orders (5,000 records)

sample_events (20,000 records)
    ↓
sample_customers (1,000 records)
```

## 📋 Table Definitions

### sample_customers
Customer dimension table with segmentation information.

| Column | Type | Description | Sample Data |
|--------|------|-------------|-------------|
| customer_id | INTEGER | Unique customer identifier | 1, 2, 3, ... |
| first_name | VARCHAR | Customer first name | James, Mary, John, ... |
| last_name | VARCHAR | Customer last name | Smith, Johnson, Williams, ... |
| email | VARCHAR | Customer email address | customer1@example.com, ... |
| phone | VARCHAR | Contact phone number | 555-100-2000, ... |
| city | VARCHAR | Customer city | New York, Los Angeles, ... |
| state | VARCHAR | Customer state | NY, CA, IL, ... |
| zip_code | VARCHAR | Postal code | 10001, 90001, ... |
| segment | VARCHAR | Customer segment | Premium, Standard, Basic, ... |
| registration_date | DATE | Registration date | 2020-01-15, ... |
| is_active | BOOLEAN | Customer active status | true, false |
| loyalty_points | INTEGER | Loyalty points balance | 1500, 5000, ... |

**Business Rules**:
- Each customer has a unique ID
- Customers are segmented into Premium, Standard, and Basic tiers
- Loyalty points range from 0 to 10,000
- Active customers have made purchases in the last 6 months

### sample_products
Product catalog with category information.

| Column | Type | Description | Sample Data |
|--------|------|-------------|-------------|
| product_id | INTEGER | Unique product identifier | 1, 2, 3, ... |
| product_name | VARCHAR | Product name | BrandA Product 1, ... |
| category | VARCHAR | Product category | Electronics, Clothing, ... |
| brand | VARCHAR | Product brand | BrandA, BrandB, ... |
| price | DECIMAL(10,2) | Product price | 99.99, 29.99, ... |
| cost | DECIMAL(10,2) | Product cost | 50.00, 15.00, ... |
| stock_quantity | INTEGER | Available stock | 100, 50, ... |
| reorder_level | INTEGER | Reorder trigger point | 10, 5, ... |
| is_available | BOOLEAN | Product availability | true, false |
| launch_date | DATE | Product launch date | 2021-01-01, ... |

**Business Rules**:
- Products belong to 10 different categories
- Price represents current selling price
- Cost represents wholesale cost
- Products with stock below reorder level need restocking
- Some products may be temporarily unavailable

### sample_orders
Order fact table with status tracking.

| Column | Type | Description | Sample Data |
|--------|------|-------------|-------------|
| order_id | INTEGER | Unique order identifier | 5001, 5002, ... |
| customer_id | INTEGER | Customer foreign key | 1, 2, 3, ... |
| product_id | INTEGER | Product foreign key | 1, 2, 3, ... |
| order_date | DATE | Order date | 2022-01-15, ... |
| delivery_date | DATE | Expected delivery date | 2022-01-20, ... |
| quantity | INTEGER | Order quantity | 1, 2, 3, ... |
| unit_price | DECIMAL(10,2) | Unit price at time of order | 99.99, 29.99, ... |
| total_amount | DECIMAL(10,2) | Total order amount | 199.98, 59.98, ... |
| status | VARCHAR | Order status | pending, processing, shipped, ... |
| payment_method | VARCHAR | Payment method | credit_card, debit_card, ... |

**Business Rules**:
- Each order links to one customer and one product
- Total amount = quantity × unit_price
- Status workflow: pending → processing → shipped → delivered (or cancelled)
- Multiple payment methods supported

### sample_transactions
Transaction details with payment information.

| Column | Type | Description | Sample Data |
|--------|------|-------------|-------------|
| transaction_id | INTEGER | Unique transaction identifier | 10001, 10002, ... |
| order_id | INTEGER | Order foreign key | 5001, 5002, ... |
| transaction_date | TIMESTAMP | Transaction timestamp | 2022-01-15 10:30:00, ... |
| amount | DECIMAL(10,2) | Transaction amount | 199.98, 59.98, ... |
| payment_method | VARCHAR | Payment method used | credit_card, debit_card, ... |
| payment_status | VARCHAR | Transaction status | success, failed, pending |
| card_last_four | VARCHAR | Last 4 digits of card | 1234, 5678, ... |
| transaction_ref | VARCHAR | Transaction reference | TXN202401190000001, ... |

**Business Rules**:
- Each order has one transaction record
- Transaction status can be success, failed, or pending
- Card information is masked for security
- Transaction references are unique identifiers

### sample_events
Web events for user engagement analysis.

| Column | Type | Description | Sample Data |
|--------|------|-------------|-------------|
| event_id | INTEGER | Unique event identifier | 1, 2, 3, ... |
| customer_id | INTEGER | Customer foreign key (nullable) | 1, 2, 3, ... |
| event_timestamp | TIMESTAMP | Event timestamp | 2023-01-15 10:30:00, ... |
| event_type | VARCHAR | Event type | page_view, click, add_to_cart, ... |
| page_url | VARCHAR | Page where event occurred | /home, /products, /cart, ... |
| referrer | VARCHAR | Traffic source | google.com, facebook.com, ... |
| browser | VARCHAR | User browser | Chrome, Firefox, Safari, ... |
| device | VARCHAR | User device type | Desktop, Mobile, Tablet |
| session_id | VARCHAR | Session identifier | session_1, session_2, ... |

**Business Rules**:
- Events can be anonymous (customer_id is null)
- Event types include page views, clicks, add to cart, purchases
- Session IDs group events by user session
- Referrer tracks traffic sources

## 🔍 Sample Queries

### Basic Queries

#### Count records in each table
```sql
SELECT 
    'customers' as table_name, COUNT(*) as record_count 
FROM sample_customers
UNION ALL
SELECT 
    'products' as table_name, COUNT(*) as record_count 
FROM sample_products
UNION ALL
SELECT 
    'orders' as table_name, COUNT(*) as record_count 
FROM sample_orders
UNION ALL
SELECT 
    'transactions' as table_name, COUNT(*) as record_count 
FROM sample_transactions
UNION ALL
SELECT 
    'events' as table_name, COUNT(*) as record_count 
FROM sample_events
```

#### Customer segmentation analysis
```sql
SELECT 
    segment,
    COUNT(*) as customer_count,
    AVG(loyalty_points) as avg_loyalty_points,
    MAX(loyalty_points) as max_loyalty_points,
    MIN(loyalty_points) as min_loyalty_points,
    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active_customers
FROM sample_customers
GROUP BY segment
ORDER BY avg_loyalty_points DESC
```

### Advanced Queries

#### Customer lifetime value calculation
```sql
WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent,
        AVG(total_amount) as avg_order_value
    FROM sample_orders
    GROUP BY customer_id
),
customer_ltv AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        c.segment,
        c.loyalty_points,
        COALESCE(co.order_count, 0) as order_count,
        COALESCE(co.total_spent, 0) as total_spent,
        COALESCE(co.avg_order_value, 0) as avg_order_value
    FROM sample_customers c
    LEFT JOIN customer_orders co ON c.customer_id = co.customer_id
)
SELECT 
    customer_id,
    first_name,
    last_name,
    segment,
    loyalty_points,
    order_count,
    total_spent,
    avg_order_value,
    CASE 
        WHEN order_count = 0 THEN 'New'
        WHEN order_count < 5 THEN 'Developing'
        WHEN order_count < 10 THEN 'Growing'
        ELSE 'Loyal'
    END as customer_stage
FROM customer_ltv
ORDER BY total_spent DESC
```

#### Product performance analysis
```sql
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    COUNT(o.order_id) as order_count,
    SUM(o.quantity) as total_quantity,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value,
    p.stock_quantity,
    p.is_available
FROM sample_products p
LEFT JOIN sample_orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name, p.category, p.brand, p.stock_quantity, p.is_available
ORDER BY total_revenue DESC
```

#### Time series analysis
```sql
SELECT 
    DATE_TRUNC('day', order_date) as day,
    COUNT(*) as order_count,
    SUM(total_amount) as daily_revenue,
    COUNT(DISTINCT customer_id) as unique_customers,
    AVG(total_amount) as avg_order_value
FROM sample_orders
WHERE order_date >= '2022-01-01'
GROUP BY day
ORDER BY day
```

## 🎯 Usage Examples

### Lab-Specific Examples

#### Lab 0: Sample Database Setup
```python
# Generate sample data
python3 scripts/generate_sample_data.py

# Load into DuckDB
python3 scripts/load_sample_data.py

# Verify data
import duckdb
con = duckdb.connect('data/duckdb_practice.db')
for table in ['sample_customers', 'sample_products', 'sample_orders', 
              'sample_transactions', 'sample_events']:
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")
```

#### Lab 3: Advanced Features
```python
# Window functions for customer ranking
import duckdb
con = duckdb.connect('data/duckdb_practice.db')

result = con.execute("""
    SELECT 
        customer_id,
        loyalty_points,
        RANK() OVER (ORDER BY loyalty_points DESC) as loyalty_rank,
        DENSE_RANK() OVER (ORDER BY loyalty_points DESC) as dense_rank,
        ROW_NUMBER() OVER (ORDER BY loyalty_points DESC) as row_num
    FROM sample_customers
    LIMIT 10
""").fetchdf()
```

#### Lab 8: Real-World Patterns
```python
# Slowly Changing Dimensions (SCD)
import duckdb
con = duckdb.connect('data/duckdb_practice.db')

# SCD Type 2 implementation
con.execute("""
    CREATE TABLE sample_customers_scd2 AS
    SELECT 
        customer_id,
        first_name,
        last_name,
        segment,
        loyalty_points,
        registration_date as effective_date,
        '9999-12-31'::DATE as end_date,
        true as is_current
    FROM sample_customers
""")
```

## 📊 Data Quality Metrics

### Completeness
- All tables have primary keys
- Foreign key relationships maintained
- No null values in critical columns

### Consistency
- Referential integrity enforced
- Business rules applied consistently
- Data types match schema definitions

### Accuracy
- Realistic business data patterns
- Appropriate data ranges
- Logical relationships between entities

### Timeliness
- Dates span realistic timeframes
- Transaction timestamps are sequential
- Event timestamps are realistic

## 🔧 Data Maintenance

### Regenerating Sample Data
```bash
# Regenerate with default settings
python3 scripts/generate_sample_data.py

# Regenerate with specific size
python3 scripts/generate_sample_data.py --size small
python3 scripts/generate_sample_data.py --size large

# Regenerate with specific seed for reproducibility
python3 scripts/generate_sample_data.py --seed 12345
```

### Reloading Data
```bash
# Reload from CSV files
python3 scripts/load_sample_data.py --format csv

# Reload from Parquet files
python3 scripts/load_sample_data.py --format parquet
```

### Data Validation
```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Check referential integrity
con.execute("""
    SELECT 'orders-customers' as relationship,
           COUNT(*) - COUNT(DISTINCT customer_id) as orphaned_records
    FROM sample_orders
""")
```

## 🎓 Learning Objectives by Table

### sample_customers
- Practice customer segmentation analysis
- Learn customer lifetime value calculation
- Practice window functions for ranking
- Understand customer lifecycle

### sample_products
- Practice product performance analysis
- Learn inventory management queries
- Practice category-based aggregations
- Understand product lifecycle

### sample_orders
- Practice order lifecycle analysis
- Learn time series analysis
- Practice order status transitions
- Understand revenue calculations

### sample_transactions
- Practice payment processing patterns
- Learn transaction reconciliation
- Practice fraud detection patterns
- Understand payment method analysis

### sample_events
- Practice user behavior analysis
- Learn session-based analytics
- Practice funnel analysis
- Understand user engagement metrics

## 🚀 Advanced Usage

### Cross-Table Analytics

#### Customer Product Affinity
```sql
SELECT 
    c.customer_id,
    c.segment,
    p.category,
    COUNT(*) as purchase_count,
    SUM(o.total_amount) as category_spend
FROM sample_customers c
JOIN sample_orders o ON c.customer_id = o.customer_id
JOIN sample_products p ON o.product_id = p.product_id
GROUP BY c.customer_id, c.segment, p.category
ORDER BY category_spend DESC
```

#### Cohort Analysis
```sql
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        MIN(order_date) as first_order_date,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM sample_orders
    GROUP BY customer_id
),
cohort_metrics AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as order_month,
        COUNT(DISTINCT c.customer_id) as customer_count,
        SUM(o.total_amount) as total_revenue
    FROM customer_cohorts c
    JOIN sample_orders o ON c.customer_id = o.customer_id
    WHERE o.order_date >= c.first_order_date
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT * FROM cohort_metrics
ORDER BY cohort_month, order_month
```

---

**This sample database provides a solid foundation for learning DuckDB and lakehouse concepts through realistic business scenarios!**