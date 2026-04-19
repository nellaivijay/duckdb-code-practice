#!/usr/bin/env python3
"""
Sample Data Generator for DuckDB Practice Environment

Generates realistic business data for hands-on learning:
- sample_customers: Customer dimension with segmentation
- sample_products: Product catalog with categories
- sample_orders: Order fact table with status tracking
- sample_transactions: Transaction details with payment methods
- sample_events: Web events for user engagement analysis
"""

import random
import datetime
import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def set_random_seed(seed):
    """Set random seed for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)


def generate_customers(num_records=1000):
    """Generate customer dimension data"""
    print(f"Generating {num_records} customers...")
    
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 
                   'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara',
                   'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah',
                   'Charles', 'Karen']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
                  'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
                  'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore',
                  'Jackson', 'Martin']
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']
    
    segments = ['Premium', 'Standard', 'Basic', 'Enterprise']
    
    data = []
    for i in range(1, num_records + 1):
        customer = {
            'customer_id': i,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'customer{i}@example.com',
            'phone': f'555-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'city': random.choice(cities),
            'state': random.choice(states),
            'zip_code': f'{random.randint(10000,99999)}',
            'segment': random.choice(segments),
            'registration_date': datetime.date(2020, 1, 1) + datetime.timedelta(days=random.randint(0, 1460)),
            'is_active': random.choice([True, True, True, False]),
            'loyalty_points': random.randint(0, 10000)
        }
        data.append(customer)
    
    return pd.DataFrame(data)


def generate_products(num_records=200):
    """Generate product catalog data"""
    print(f"Generating {num_records} products...")
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books',
                 'Toys', 'Food & Beverages', 'Health & Wellness', 'Automotive', 'Office']
    
    brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
    
    data = []
    for i in range(1, num_records + 1):
        product = {
            'product_id': i,
            'product_name': f'{random.choice(brands)} Product {i}',
            'category': random.choice(categories),
            'brand': random.choice(brands),
            'price': round(random.uniform(10.0, 500.0), 2),
            'cost': round(random.uniform(5.0, 250.0), 2),
            'stock_quantity': random.randint(0, 1000),
            'reorder_level': random.randint(10, 50),
            'is_available': random.choice([True, True, True, False]),
            'launch_date': datetime.date(2021, 1, 1) + datetime.timedelta(days=random.randint(0, 1095))
        }
        data.append(product)
    
    return pd.DataFrame(data)


def generate_orders(num_records=5000, num_customers=1000, num_products=200):
    """Generate order fact table data"""
    print(f"Generating {num_records} orders...")
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    data = []
    for i in range(1, num_records + 1):
        order_date = datetime.date(2022, 1, 1) + datetime.timedelta(days=random.randint(0, 730))
        delivery_date = order_date + datetime.timedelta(days=random.randint(1, 14)) if random.random() > 0.2 else None
        
        order = {
            'order_id': i,
            'customer_id': random.randint(1, num_customers),
            'product_id': random.randint(1, num_products),
            'order_date': order_date,
            'delivery_date': delivery_date,
            'quantity': random.randint(1, 10),
            'unit_price': round(random.uniform(10.0, 500.0), 2),
            'total_amount': 0.0,  # Will be calculated
            'status': random.choice(statuses),
            'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'bank_transfer'])
        }
        order['total_amount'] = round(order['quantity'] * order['unit_price'], 2)
        data.append(order)
    
    return pd.DataFrame(data)


def generate_transactions(num_records=10000, num_orders=5000):
    """Generate transaction details data"""
    print(f"Generating {num_records} transactions...")
    
    payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'apple_pay']
    
    data = []
    for i in range(1, num_records + 1):
        transaction = {
            'transaction_id': i,
            'order_id': random.randint(1, num_orders),
            'transaction_date': datetime.datetime(2022, 1, 1) + datetime.timedelta(days=random.randint(0, 730),
                                                                                   hours=random.randint(0, 23),
                                                                                   minutes=random.randint(0, 59)),
            'amount': round(random.uniform(10.0, 1000.0), 2),
            'payment_method': random.choice(payment_methods),
            'payment_status': random.choice(['success', 'success', 'success', 'failed', 'pending']),
            'card_last_four': f'{random.randint(1000,9999)}' if random.choice([True, False]) else None,
            'transaction_ref': f'TXN{datetime.datetime.now().strftime("%Y%m%d")}{i:06d}'
        }
        data.append(transaction)
    
    return pd.DataFrame(data)


def generate_events(num_records=20000, num_customers=1000):
    """Generate web event data for user engagement analysis"""
    print(f"Generating {num_records} events...")
    
    event_types = ['page_view', 'click', 'add_to_cart', 'purchase', 'search', 'login', 'logout']
    
    pages = ['/home', '/products', '/cart', '/checkout', '/account', '/search', '/about']
    
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Mobile']
    
    devices = ['Desktop', 'Mobile', 'Tablet']
    
    data = []
    for i in range(1, num_records + 1):
        event = {
            'event_id': i,
            'customer_id': random.randint(1, num_customers) if random.random() > 0.3 else None,
            'event_timestamp': datetime.datetime(2023, 1, 1) + datetime.timedelta(days=random.randint(0, 365),
                                                                                   hours=random.randint(0, 23),
                                                                                   minutes=random.randint(0, 59),
                                                                                   seconds=random.randint(0, 59)),
            'event_type': random.choice(event_types),
            'page_url': random.choice(pages),
            'referrer': random.choice(['google.com', 'facebook.com', 'twitter.com', 'direct', None]),
            'browser': random.choice(browsers),
            'device': random.choice(devices),
            'session_id': f'session_{random.randint(1, 5000)}'
        }
        data.append(event)
    
    return pd.DataFrame(data)


def main():
    parser = argparse.ArgumentParser(description='Generate sample data for DuckDB practice')
    parser.add_argument('--size', choices=['small', 'medium', 'large'], default='medium',
                       help='Size of sample dataset')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--output-dir', type=str, default='data/sample', help='Output directory for data files')
    
    args = parser.parse_args()
    
    # Set size parameters
    size_params = {
        'small': {'customers': 500, 'products': 100, 'orders': 2500, 'transactions': 5000, 'events': 10000},
        'medium': {'customers': 1000, 'products': 200, 'orders': 5000, 'transactions': 10000, 'events': 20000},
        'large': {'customers': 5000, 'products': 1000, 'orders': 25000, 'transactions': 50000, 'events': 100000}
    }
    
    params = size_params[args.size]
    
    # Set random seed
    set_random_seed(args.seed)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating sample data with {args.size} size (seed: {args.seed})")
    print(f"Output directory: {output_dir}")
    
    # Generate datasets
    customers_df = generate_customers(params['customers'])
    products_df = generate_products(params['products'])
    orders_df = generate_orders(params['orders'], params['customers'], params['products'])
    transactions_df = generate_transactions(params['transactions'], params['orders'])
    events_df = generate_events(params['events'], params['customers'])
    
    # Save to CSV files
    customers_df.to_csv(output_dir / 'customers.csv', index=False)
    products_df.to_csv(output_dir / 'products.csv', index=False)
    orders_df.to_csv(output_dir / 'orders.csv', index=False)
    transactions_df.to_csv(output_dir / 'transactions.csv', index=False)
    events_df.to_csv(output_dir / 'events.csv', index=False)
    
    # Save to Parquet files
    customers_df.to_parquet(output_dir / 'customers.parquet', index=False)
    products_df.to_parquet(output_dir / 'products.parquet', index=False)
    orders_df.to_parquet(output_dir / 'orders.parquet', index=False)
    transactions_df.to_parquet(output_dir / 'transactions.parquet', index=False)
    events_df.to_parquet(output_dir / 'events.parquet', index=False)
    
    print(f"\nSample data generation complete!")
    print(f"Generated {params['customers']} customers")
    print(f"Generated {params['products']} products")
    print(f"Generated {params['orders']} orders")
    print(f"Generated {params['transactions']} transactions")
    print(f"Generated {params['events']} events")
    print(f"\nFiles saved to: {output_dir}")
    print(f"Format: CSV and Parquet")


if __name__ == '__main__':
    main()