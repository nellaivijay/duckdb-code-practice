#!/usr/bin/env python3
"""
Sample Data Loader for DuckDB Practice Environment

Loads generated sample data into DuckDB database for hands-on learning.
"""

import duckdb
import argparse
from pathlib import Path


def create_database_schema(con):
    """Create database schema for sample data"""
    print("Creating database schema...")
    
    # Create customers table
    con.execute("""
        CREATE TABLE IF NOT EXISTS sample_customers (
            customer_id INTEGER PRIMARY KEY,
            first_name VARCHAR,
            last_name VARCHAR,
            email VARCHAR,
            phone VARCHAR,
            city VARCHAR,
            state VARCHAR,
            zip_code VARCHAR,
            segment VARCHAR,
            registration_date DATE,
            is_active BOOLEAN,
            loyalty_points INTEGER
        )
    """)
    
    # Create products table
    con.execute("""
        CREATE TABLE IF NOT EXISTS sample_products (
            product_id INTEGER PRIMARY KEY,
            product_name VARCHAR,
            category VARCHAR,
            brand VARCHAR,
            price DECIMAL(10,2),
            cost DECIMAL(10,2),
            stock_quantity INTEGER,
            reorder_level INTEGER,
            is_available BOOLEAN,
            launch_date DATE
        )
    """)
    
    # Create orders table
    con.execute("""
        CREATE TABLE IF NOT EXISTS sample_orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            order_date DATE,
            delivery_date DATE,
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            status VARCHAR,
            payment_method VARCHAR,
            FOREIGN KEY (customer_id) REFERENCES sample_customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES sample_products(product_id)
        )
    """)
    
    # Create transactions table
    con.execute("""
        CREATE TABLE IF NOT EXISTS sample_transactions (
            transaction_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            transaction_date TIMESTAMP,
            amount DECIMAL(10,2),
            payment_method VARCHAR,
            payment_status VARCHAR,
            card_last_four VARCHAR,
            transaction_ref VARCHAR,
            FOREIGN KEY (order_id) REFERENCES sample_orders(order_id)
        )
    """)
    
    # Create events table
    con.execute("""
        CREATE TABLE IF NOT EXISTS sample_events (
            event_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            event_timestamp TIMESTAMP,
            event_type VARCHAR,
            page_url VARCHAR,
            referrer VARCHAR,
            browser VARCHAR,
            device VARCHAR,
            session_id VARCHAR,
            FOREIGN KEY (customer_id) REFERENCES sample_customers(customer_id)
        )
    """)
    
    print("Schema created successfully!")


def load_data_from_csv(con, data_dir):
    """Load data from CSV files"""
    print("Loading data from CSV files...")
    
    data_path = Path(data_dir)
    
    # Load customers
    if (data_path / 'customers.csv').exists():
        con.execute(f"COPY sample_customers FROM '{data_path / 'customers.csv'}' (HEADER, DELIMITER ',')")
        print(f"Loaded customers from CSV")
    
    # Load products
    if (data_path / 'products.csv').exists():
        con.execute(f"COPY sample_products FROM '{data_path / 'products.csv'}' (HEADER, DELIMITER ',')")
        print(f"Loaded products from CSV")
    
    # Load orders
    if (data_path / 'orders.csv').exists():
        con.execute(f"COPY sample_orders FROM '{data_path / 'orders.csv'}' (HEADER, DELIMITER ',')")
        print(f"Loaded orders from CSV")
    
    # Load transactions
    if (data_path / 'transactions.csv').exists():
        con.execute(f"COPY sample_transactions FROM '{data_path / 'transactions.csv'}' (HEADER, DELIMITER ',')")
        print(f"Loaded transactions from CSV")
    
    # Load events
    if (data_path / 'events.csv').exists():
        con.execute(f"COPY sample_events FROM '{data_path / 'events.csv'}' (HEADER, DELIMITER ',')")
        print(f"Loaded events from CSV")


def load_data_from_parquet(con, data_dir):
    """Load data from Parquet files"""
    print("Loading data from Parquet files...")
    
    data_path = Path(data_dir)
    
    # Load customers
    if (data_path / 'customers.parquet').exists():
        con.execute(f"COPY sample_customers FROM '{data_path / 'customers.parquet'}' (FORMAT PARQUET)")
        print(f"Loaded customers from Parquet")
    
    # Load products
    if (data_path / 'products.parquet').exists():
        con.execute(f"COPY sample_products FROM '{data_path / 'products.parquet'}' (FORMAT PARQUET)")
        print(f"Loaded products from Parquet")
    
    # Load orders
    if (data_path / 'orders.parquet').exists():
        con.execute(f"COPY sample_orders FROM '{data_path / 'orders.parquet'}' (FORMAT PARQUET)")
        print(f"Loaded orders from Parquet")
    
    # Load transactions
    if (data_path / 'transactions.parquet').exists():
        con.execute(f"COPY sample_transactions FROM '{data_path / 'transactions.parquet'}' (FORMAT PARQUET)")
        print(f"Loaded transactions from Parquet")
    
    # Load events
    if (data_path / 'events.parquet').exists():
        con.execute(f"COPY sample_events FROM '{data_path / 'events.parquet'}' (FORMAT PARQUET)")
        print(f"Loaded events from Parquet")


def create_indexes(con):
    """Create indexes for better query performance"""
    print("Creating indexes...")
    
    # Create indexes on foreign keys
    con.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON sample_orders(customer_id)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_orders_product ON sample_orders(product_id)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON sample_orders(order_date)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_transactions_order ON sample_transactions(order_id)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_events_customer ON sample_events(customer_id)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON sample_events(event_timestamp)")
    
    print("Indexes created successfully!")


def verify_data(con):
    """Verify data was loaded correctly"""
    print("Verifying data...")
    
    # Check row counts
    tables = ['sample_customers', 'sample_products', 'sample_orders', 
              'sample_transactions', 'sample_events']
    
    for table in tables:
        result = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        print(f"{table}: {result[0]} rows")
    
    # Sample queries
    print("\nSample queries:")
    
    # Customer segment distribution
    segments = con.execute("""
        SELECT segment, COUNT(*) as count 
        FROM sample_customers 
        GROUP BY segment 
        ORDER BY count DESC
    """).fetchall()
    print("Customer segments:", segments)
    
    # Product category distribution
    categories = con.execute("""
        SELECT category, COUNT(*) as count 
        FROM sample_products 
        GROUP BY category 
        ORDER BY count DESC
    """).fetchall()
    print("Product categories:", categories[:5])
    
    # Order status distribution
    statuses = con.execute("""
        SELECT status, COUNT(*) as count 
        FROM sample_orders 
        GROUP BY status 
        ORDER BY count DESC
    """).fetchall()
    print("Order statuses:", statuses)


def main():
    parser = argparse.ArgumentParser(description='Load sample data into DuckDB database')
    parser.add_argument('--database', type=str, default='data/duckdb_practice.db',
                       help='Path to DuckDB database file')
    parser.add_argument('--data-dir', type=str, default='data/sample',
                       help='Directory containing sample data files')
    parser.add_argument('--format', choices=['csv', 'parquet', 'both'], default='parquet',
                       help='Format of data files to load')
    
    args = parser.parse_args()
    
    # Create data directory if it doesn't exist
    Path(args.database).parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading sample data into DuckDB database: {args.database}")
    print(f"Data directory: {args.data_dir}")
    print(f"Data format: {args.format}")
    
    # Connect to database
    con = duckdb.connect(args.database)
    
    try:
        # Create schema
        create_database_schema(con)
        
        # Load data based on format preference
        if args.format in ['parquet', 'both']:
            load_data_from_parquet(con, args.data_dir)
        if args.format in ['csv', 'both']:
            load_data_from_csv(con, args.data_dir)
        
        # Create indexes
        create_indexes(con)
        
        # Verify data
        verify_data(con)
        
        print(f"\nSample data loaded successfully into {args.database}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        raise
    finally:
        con.close()


if __name__ == '__main__':
    main()