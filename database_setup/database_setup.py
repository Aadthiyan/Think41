import sqlite3
import pandas as pd
import os
from pathlib import Path

def create_database():
    """Create the database and products table"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            cost REAL,
            category TEXT,
            name TEXT,
            brand TEXT,
            retail_price REAL,
            department TEXT,
            sku TEXT,
            distribution_center_id INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and products table created successfully!")

def load_products_data():
    """Load products data from CSV into the database"""
    csv_path = Path('../archive/products.csv')
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found!")
        return False
    
    try:
        # Read CSV file
        print("Reading products.csv...")
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} products in the CSV file")
        
        # Connect to database
        conn = sqlite3.connect('ecommerce.db')
        
        # Load data into database
        print("Loading data into database...")
        df.to_sql('products', conn, if_exists='replace', index=False)
        
        conn.close()
        print("Data loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def verify_data():
    """Verify that the data was loaded correctly"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Get total count
    cursor.execute('SELECT COUNT(*) FROM products')
    total_count = cursor.fetchone()[0]
    print(f"Total products in database: {total_count}")
    
    # Get sample data
    cursor.execute('SELECT * FROM products LIMIT 5')
    sample_data = cursor.fetchall()
    print("\nSample data:")
    for row in sample_data:
        print(f"ID: {row[0]}, Name: {row[3]}, Brand: {row[4]}, Price: ${row[5]}")
    
    # Get some statistics
    cursor.execute('SELECT COUNT(DISTINCT category) FROM products')
    categories = cursor.fetchone()[0]
    print(f"\nNumber of categories: {categories}")
    
    cursor.execute('SELECT COUNT(DISTINCT brand) FROM products')
    brands = cursor.fetchone()[0]
    print(f"Number of brands: {brands}")
    
    cursor.execute('SELECT COUNT(DISTINCT department) FROM products')
    departments = cursor.fetchone()[0]
    print(f"Number of departments: {departments}")
    
    conn.close()

def main():
    print("=== E-commerce Database Setup ===")
    print("Step 1: Creating database and table...")
    create_database()
    
    print("\nStep 2: Loading products data...")
    if load_products_data():
        print("\nStep 3: Verifying data...")
        verify_data()
        print("\n=== Setup Complete! ===")
    else:
        print("Failed to load data. Please check the CSV file.")

if __name__ == "__main__":
    main() 