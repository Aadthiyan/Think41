import sqlite3
import pandas as pd

def query_database():
    """Demonstrate various queries on the products database"""
    conn = sqlite3.connect('ecommerce.db')
    
    print("=== Database Query Examples ===\n")
    
    # 1. Total number of products
    total_products = pd.read_sql_query("SELECT COUNT(*) as total FROM products", conn)
    print(f"1. Total Products: {total_products['total'].iloc[0]}")
    
    # 2. Products by department
    dept_stats = pd.read_sql_query("""
        SELECT department, COUNT(*) as count 
        FROM products 
        GROUP BY department
    """, conn)
    print(f"\n2. Products by Department:")
    print(dept_stats.to_string(index=False))
    
    # 3. Top 5 brands by product count
    top_brands = pd.read_sql_query("""
        SELECT brand, COUNT(*) as product_count 
        FROM products 
        GROUP BY brand 
        ORDER BY product_count DESC 
        LIMIT 5
    """, conn)
    print(f"\n3. Top 5 Brands by Product Count:")
    print(top_brands.to_string(index=False))
    
    # 4. Price range statistics
    price_stats = pd.read_sql_query("""
        SELECT 
            MIN(retail_price) as min_price,
            MAX(retail_price) as max_price,
            AVG(retail_price) as avg_price,
            COUNT(*) as total_products
        FROM products
    """, conn)
    print(f"\n4. Price Statistics:")
    print(f"   Min Price: ${price_stats['min_price'].iloc[0]:.2f}")
    print(f"   Max Price: ${price_stats['max_price'].iloc[0]:.2f}")
    print(f"   Avg Price: ${price_stats['avg_price'].iloc[0]:.2f}")
    print(f"   Total Products: {price_stats['total_products'].iloc[0]}")
    
    # 5. Sample products
    sample_products = pd.read_sql_query("""
        SELECT id, name, brand, retail_price, category 
        FROM products 
        ORDER BY RANDOM() 
        LIMIT 3
    """, conn)
    print(f"\n5. Sample Products:")
    for _, row in sample_products.iterrows():
        print(f"   ID: {row['id']}, Name: {row['name'][:50]}..., Brand: {row['brand']}, Price: ${row['retail_price']:.2f}")
    
    conn.close()

if __name__ == "__main__":
    query_database() 