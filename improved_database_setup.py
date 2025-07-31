import sqlite3
import pandas as pd
import os
from pathlib import Path

def create_improved_database():
    """Create the database with improved schema based on CSV analysis"""
    conn = sqlite3.connect('ecommerce_improved.db')
    cursor = conn.cursor()
    
    # Create products table with better data types and constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            cost REAL NOT NULL CHECK (cost >= 0),
            category TEXT NOT NULL CHECK (length(category) <= 50),
            name TEXT CHECK (length(name) <= 500),
            brand TEXT CHECK (length(brand) <= 100),
            retail_price REAL NOT NULL CHECK (retail_price >= 0),
            department TEXT NOT NULL CHECK (department IN ('Men', 'Women')),
            sku TEXT NOT NULL CHECK (length(sku) = 32) UNIQUE,
            distribution_center_id INTEGER NOT NULL CHECK (distribution_center_id BETWEEN 1 AND 10)
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_department ON products(department)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_price ON products(retail_price)')
    
    conn.commit()
    conn.close()
    print("Improved database and products table created successfully!")

def load_products_data_improved():
    """Load products data with data cleaning and validation"""
    csv_path = Path('archive/products.csv')
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found!")
        return False
    
    try:
        # Read CSV file
        print("Reading products.csv...")
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} products in the CSV file")
        
        # Data cleaning
        print("Cleaning data...")
        
        # Handle null values
        df['name'] = df['name'].fillna('Unknown Product')
        df['brand'] = df['brand'].fillna('Unknown Brand')
        
        # Ensure SKU is exactly 32 characters (pad or truncate if needed)
        df['sku'] = df['sku'].astype(str).str[:32].str.pad(32, side='right', fillchar='0')
        
        # Validate price constraints
        df = df[df['cost'] >= 0]
        df = df[df['retail_price'] >= 0]
        
        # Validate department values
        df = df[df['department'].isin(['Men', 'Women'])]
        
        # Validate distribution center IDs
        df = df[df['distribution_center_id'].between(1, 10)]
        
        print(f"After cleaning: {len(df)} products")
        
        # Connect to database
        conn = sqlite3.connect('ecommerce_improved.db')
        
        # Load data into database
        print("Loading data into improved database...")
        df.to_sql('products', conn, if_exists='replace', index=False)
        
        conn.close()
        print("Data loaded successfully into improved database!")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def verify_improved_data():
    """Verify the data with improved validation"""
    conn = sqlite3.connect('ecommerce_improved.db')
    cursor = conn.cursor()
    
    print("\n=== Improved Database Verification ===")
    
    # Get total count
    cursor.execute('SELECT COUNT(*) FROM products')
    total_count = cursor.fetchone()[0]
    print(f"Total products in database: {total_count}")
    
    # Check data integrity
    cursor.execute('SELECT COUNT(*) FROM products WHERE cost < 0 OR retail_price < 0')
    invalid_prices = cursor.fetchone()[0]
    print(f"Products with invalid prices: {invalid_prices}")
    
    cursor.execute('SELECT COUNT(*) FROM products WHERE department NOT IN ("Men", "Women")')
    invalid_depts = cursor.fetchone()[0]
    print(f"Products with invalid departments: {invalid_depts}")
    
    cursor.execute('SELECT COUNT(*) FROM products WHERE length(sku) != 32')
    invalid_skus = cursor.fetchone()[0]
    print(f"Products with invalid SKU length: {invalid_skus}")
    
    # Get sample data
    cursor.execute('SELECT id, name, brand, retail_price, category FROM products LIMIT 3')
    sample_data = cursor.fetchall()
    print("\nSample data:")
    for row in sample_data:
        print(f"ID: {row[0]}, Name: {row[1][:50]}..., Brand: {row[2]}, Price: ${row[3]:.2f}")
    
    # Get statistics
    cursor.execute('SELECT COUNT(DISTINCT category) FROM products')
    categories = cursor.fetchone()[0]
    print(f"\nNumber of categories: {categories}")
    
    cursor.execute('SELECT COUNT(DISTINCT brand) FROM products')
    brands = cursor.fetchone()[0]
    print(f"Number of brands: {brands}")
    
    cursor.execute('SELECT COUNT(DISTINCT department) FROM products')
    departments = cursor.fetchone()[0]
    print(f"Number of departments: {departments}")
    
    # Price statistics
    cursor.execute('''
        SELECT 
            MIN(retail_price) as min_price,
            MAX(retail_price) as max_price,
            AVG(retail_price) as avg_price
        FROM products
    ''')
    price_stats = cursor.fetchone()
    print(f"Price range: ${price_stats[0]:.2f} - ${price_stats[1]:.2f} (avg: ${price_stats[2]:.2f})")
    
    conn.close()

def main():
    print("=== Improved E-commerce Database Setup ===")
    print("Step 1: Creating improved database and table...")
    create_improved_database()
    
    print("\nStep 2: Loading products data with validation...")
    if load_products_data_improved():
        print("\nStep 3: Verifying improved data...")
        verify_improved_data()
        print("\n=== Improved Setup Complete! ===")
    else:
        print("Failed to load data. Please check the CSV file.")

if __name__ == "__main__":
    main() 