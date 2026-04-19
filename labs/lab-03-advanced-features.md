# Lab 3: Advanced Features and Capabilities

## 🎯 Learning Objectives

- Master window functions and analytical queries
- Understand complex join strategies and performance
- Work with subqueries, CTEs, and advanced SQL patterns
- Practice data type conversions and casting
- Learn about DuckDB's advanced SQL capabilities

## 📋 Prerequisites

- Completed Lab 2: Basic Operations
- Working DuckDB environment
- Sample database loaded

## ⏱️ Estimated Time

45-60 minutes

## 🎓 Conceptual Background

DuckDB provides advanced SQL features that enable complex analytical queries and data transformations. This lab covers:

**Window Functions**: Perform calculations across rows related to the current row
**Advanced Joins**: Different join strategies and their performance implications
**Subqueries & CTEs**: Complex query patterns and readability
**Data Type Handling**: Conversions and casting between types
**Lakehouse Patterns**: How DuckDB fits into modern lakehouse architectures

## 🚀 Step-by-Step Instructions

### Step 1: Window Functions

Window functions allow you to perform calculations across a set of rows related to the current row.

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Basic window function - ranking
result = con.execute("""
    SELECT customer_id, loyalty_points,
           RANK() OVER (ORDER BY loyalty_points DESC) as loyalty_rank
    FROM sample_customers
    LIMIT 10
""").fetchall()
print("Customer loyalty rankings:", result)

# Window function with partitioning
result = con.execute("""
    SELECT segment, customer_id, loyalty_points,
           AVG(loyalty_points) OVER (PARTITION BY segment) as segment_avg
    FROM sample_customers
    LIMIT 10
""").fetchall()
print("Segment averages:", result)

# Moving average (time series)
result = con.execute("""
    SELECT order_id, order_date, total_amount,
           AVG(total_amount) OVER (
               ORDER BY order_date 
               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
           ) as moving_avg
    FROM sample_orders
    WHERE order_date >= '2022-01-01'
    LIMIT 10
""").fetchall()
print("Moving average:", result)
```

### Step 2: Advanced Join Strategies

Understand different join types and their performance characteristics.

```python
# Inner join with multiple conditions
result = con.execute("""
    SELECT c.customer_id, c.first_name, c.last_name, o.order_id, o.total_amount
    FROM sample_customers c
    INNER JOIN sample_orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'delivered'
    LIMIT 10
""").fetchall()
print("Customers with delivered orders:", result)

# Left join to find customers without orders
result = con.execute("""
    SELECT c.customer_id, c.first_name, c.last_name, o.order_id
    FROM sample_customers c
    LEFT JOIN sample_orders o ON c.customer_id = o.customer_id
    WHERE o.order_id IS NULL
    LIMIT 10
""").fetchall()
print("Customers without orders:", result)

# Self join for hierarchical data
result = con.execute("""
    SELECT c1.customer_id, c1.first_name, c2.customer_id as related_customer, c2.first_name as related_name
    FROM sample_customers c1
    INNER JOIN sample_customers c2 ON c1.segment = c2.segment AND c1.customer_id != c2.customer_id
    LIMIT 10
""").fetchall()
print("Related customers in same segment:", result)

# Cross join for combinations
result = con.execute("""
    SELECT c.segment, p.category, COUNT(*) as potential_combinations
    FROM sample_customers c
    CROSS JOIN sample_products p
    GROUP BY c.segment, p.category
    LIMIT 10
""").fetchall()
print("Segment-category combinations:", result)
```

### Step 3: Subqueries and CTEs

Complex query patterns using subqueries and Common Table Expressions.

```python
# Subquery in WHERE clause
result = con.execute("""
    SELECT customer_id, first_name, loyalty_points
    FROM sample_customers
    WHERE loyalty_points > (
        SELECT AVG(loyalty_points) FROM sample_customers
    )
    LIMIT 10
""").fetchall()
print("Customers above average loyalty:", result)

# Subquery in FROM clause (derived table)
result = con.execute("""
    SELECT segment, avg_loyalty
    FROM (
        SELECT segment, AVG(loyalty_points) as avg_loyalty
        FROM sample_customers
        GROUP BY segment
    ) as segment_stats
    ORDER BY avg_loyalty DESC
""").fetchall()
print("Segment loyalty averages:", result)

# CTE (Common Table Expression)
result = con.execute("""
    WITH customer_stats AS (
        SELECT customer_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
        FROM sample_orders
        GROUP BY customer_id
    )
    SELECT c.customer_id, c.first_name, cs.order_count, cs.total_spent
    FROM sample_customers c
    LEFT JOIN customer_stats cs ON c.customer_id = cs.customer_id
    ORDER BY cs.total_spent DESC NULLS LAST
    LIMIT 10
""").fetchall()
print("Customer spending analysis:", result)

# Multiple CTEs for complex analysis
result = con.execute("""
    WITH daily_revenue AS (
        SELECT order_date, SUM(total_amount) as daily_total
        FROM sample_orders
        WHERE status = 'delivered'
        GROUP BY order_date
    ),
    running_total AS (
        SELECT order_date, daily_total,
               SUM(daily_total) OVER (ORDER BY order_date) as cumulative_revenue
        FROM daily_revenue
    )
    SELECT * FROM running_total
    ORDER BY order_date
    LIMIT 10
""").fetchall()
print("Cumulative revenue analysis:", result)
```

### Step 4: Data Type Conversions

Handle data type conversions and casting operations.

```python
# Explicit type casting
result = con.execute("""
    SELECT customer_id, 
           CAST(loyalty_points AS VARCHAR) as points_string,
           CAST(loyalty_points AS DOUBLE) / 100.0 as points_hundreds
    FROM sample_customers
    LIMIT 5
""").fetchall()
print("Type casting examples:", result)

# Date/time conversions
result = con.execute("""
    SELECT order_id, order_date,
           EXTRACT(YEAR FROM order_date) as order_year,
           EXTRACT(MONTH FROM order_date) as order_month,
           EXTRACT(DAY FROM order_date) as order_day
    FROM sample_orders
    LIMIT 5
""").fetchall()
print("Date extraction:", result)

# String to date conversion
result = con.execute("""
    SELECT order_id, order_date,
           DATE_FORMAT(order_date, '%Y-%m') as year_month,
           DATE_TRUNC('month', order_date) as month_start
    FROM sample_orders
    LIMIT 5
""").fetchall()
print("Date formatting:", result)

# Conditional type handling
result = con.execute("""
    SELECT customer_id, loyalty_points,
           CASE 
               WHEN loyalty_points > 5000 THEN 'High'
               WHEN loyalty_points > 2000 THEN 'Medium'
               ELSE 'Low'
           END as loyalty_tier
    FROM sample_customers
    LIMIT 10
""").fetchall()
print("Conditional classification:", result)
```

### Step 5: Lakehouse Architecture Patterns

Understand how DuckDB fits into modern lakehouse architectures.

```python
# Lakehouse pattern: Bronze, Silver, Gold layers
# Bronze layer: Raw data
bronze_data = con.execute("""
    SELECT * FROM sample_orders
    WHERE order_date >= '2022-01-01'
""").df()

print("Bronze layer (raw data):", bronze_data.shape)

# Silver layer: Cleaned and validated
silver_data = con.execute("""
    SELECT order_id, customer_id, order_date, total_amount, status,
           CASE 
               WHEN total_amount <= 0 THEN NULL
               ELSE total_amount
           END as validated_amount,
           CASE 
               WHEN status NOT IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled') THEN 'unknown'
               ELSE status
           END as validated_status
    FROM sample_orders
    WHERE order_date >= '2022-01-01'
""").df()

print("Silver layer (validated):", silver_data.shape)

# Gold layer: Aggregated and business-ready
gold_data = con.execute("""
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        COUNT(*) as total_orders,
        SUM(validated_amount) as total_revenue,
        AVG(validated_amount) as avg_order_value,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM (
        SELECT order_id, customer_id, order_date, total_amount, status,
               CASE 
                   WHEN total_amount <= 0 THEN NULL
                   ELSE total_amount
               END as validated_amount
        FROM sample_orders
        WHERE order_date >= '2022-01-01'
    ) silver_layer
    GROUP BY month
    ORDER BY month
""").df()

print("Gold layer (aggregated):", gold_data.shape)
print("Monthly analytics:", gold_data.head())
```

## 💻 Hands-On Exercises

### Exercise 1: Customer Segmentation with Window Functions

Create a customer segmentation model using RFM (Recency, Frequency, Monetary) analysis:

```python
# Your code here
# Calculate recency (days since last order)
# Calculate frequency (number of orders)
# Calculate monetary (total spending)
# Use window functions to create customer segments
```

### Exercise 2: Complex Join Analysis

Analyze customer behavior across multiple dimensions:

```python
# Your code here
# Join customers, orders, and transactions
# Find patterns in customer behavior
# Identify high-value customers
# Analyze customer retention
```

### Exercise 3: Advanced CTE Patterns

Create a complex analysis using multiple CTEs:

```python
# Your code here
# Analyze product performance over time
# Calculate running totals and moving averages
# Identify seasonal patterns
# Compare performance across categories
```

### Exercise 4: Data Quality Validation

Implement data quality checks using advanced SQL:

```python
# Your code here
# Check for duplicate records
# Validate referential integrity
# Identify data anomalies
# Create data quality reports
```

### Exercise 5: Lakehouse Pipeline Design

Design a lakehouse pipeline for the sample data:

```python
# Your code here
# Design bronze, silver, gold layers
# Implement data transformations
# Create business metrics
# Build data quality checks
```

## ✅ Expected Results

After completing this lab, you should:

1. ✅ Be proficient with window functions and analytical queries
2. ✅ Understand different join strategies and performance
3. ✅ Be able to write complex queries with subqueries and CTEs
4. ✅ Handle data type conversions effectively
5. ✅ Understand lakehouse architecture patterns
6. ✅ Be able to design multi-layer data pipelines

## 🔍 Verification

Test your advanced SQL skills:

```python
import duckdb

con = duckdb.connect('data/duckdb_practice.db')

# Test window functions
result = con.execute("""
    SELECT customer_id, loyalty_points,
           RANK() OVER (ORDER BY loyalty_points DESC) as rank
    FROM sample_customers
    LIMIT 5
""").fetchall()
print("Window function test:", result)

# Test complex joins
result = con.execute("""
    SELECT c.customer_id, COUNT(DISTINCT o.order_id) as order_count
    FROM sample_customers c
    LEFT JOIN sample_orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    LIMIT 5
""").fetchall()
print("Complex join test:", result)

# Test CTEs
result = con.execute("""
    WITH order_stats AS (
        SELECT customer_id, COUNT(*) as orders, SUM(total_amount) as total
        FROM sample_orders
        GROUP BY customer_id
    )
    SELECT * FROM order_stats LIMIT 5
""").fetchall()
print("CTE test:", result)

print("✅ Advanced features test completed successfully!")
```

## 🆘 Troubleshooting

### Issue: Window function performance

**Solution**: Use appropriate window frames and indexing:
```python
# Add indexes on columns used in window functions
con.execute("CREATE INDEX idx_customers_loyalty ON sample_customers(loyalty_points)")
```

### Issue: Complex query performance

**Solution**: Break complex queries into smaller CTEs and add indexes:
```python
# Use CTEs for better optimization
# Add indexes on join columns
con.execute("CREATE INDEX idx_orders_customer ON sample_orders(customer_id)")
```

### Issue: Type conversion errors

**Solution**: Use explicit casting and handle NULL values:
```python
# Use COALESCE for NULL handling
con.execute("SELECT COALESCE(CAST(column AS VARCHAR), 'N/A') FROM table")
```

## 📚 Next Steps

After completing this lab:

1. **Proceed to Lab 4**: DuckDB + Python Integration
2. **Learn lakehouse patterns**: Study modern data architecture
3. **Practice optimization**: Learn query performance tuning
4. **Build pipelines**: Apply patterns to real data

---

**You now have advanced DuckDB skills and understand lakehouse architecture patterns!**