import sqlite3
import pandas as pd

def detailed_query_demo():
    """Detailed query demonstration for presentation"""
    
    print("=" * 70)
    print("📊 DETAILED DATABASE QUERIES - SAMPLE DATA OUTPUT")
    print("=" * 70)
    
    conn = sqlite3.connect('ecommerce_improved.db')
    
    # 1. Basic Statistics
    print("\n1️⃣ BASIC STATISTICS")
    print("-" * 50)
    
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM products')
    total = cursor.fetchone()[0]
    print(f"📦 Total Products: {total:,}")
    
    cursor.execute('SELECT COUNT(DISTINCT category) FROM products')
    categories = cursor.fetchone()[0]
    print(f"🏷️  Unique Categories: {categories}")
    
    cursor.execute('SELECT COUNT(DISTINCT brand) FROM products')
    brands = cursor.fetchone()[0]
    print(f"🏪 Unique Brands: {brands:,}")
    
    # 2. Department Distribution
    print("\n2️⃣ DEPARTMENT DISTRIBUTION")
    print("-" * 50)
    
    dept_query = """
    SELECT department, COUNT(*) as count, 
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 2) as percentage
    FROM products 
    GROUP BY department
    ORDER BY count DESC
    """
    dept_data = pd.read_sql_query(dept_query, conn)
    print(dept_data.to_string(index=False))
    
    # 3. Price Analysis
    print("\n3️⃣ PRICE ANALYSIS")
    print("-" * 50)
    
    price_query = """
    SELECT 
        MIN(retail_price) as min_price,
        MAX(retail_price) as max_price,
        ROUND(AVG(retail_price), 2) as avg_price
    FROM products
    """
    price_data = pd.read_sql_query(price_query, conn)
    print(f"💰 Price Statistics:")
    print(f"   Minimum: ${price_data['min_price'].iloc[0]:.2f}")
    print(f"   Maximum: ${price_data['max_price'].iloc[0]:.2f}")
    print(f"   Average: ${price_data['avg_price'].iloc[0]:.2f}")
    
    # 4. Top Brands
    print("\n4️⃣ TOP 10 BRANDS BY PRODUCT COUNT")
    print("-" * 50)
    
    brand_query = """
    SELECT brand, COUNT(*) as product_count
    FROM products 
    GROUP BY brand 
    ORDER BY product_count DESC 
    LIMIT 10
    """
    brand_data = pd.read_sql_query(brand_query, conn)
    print(brand_data.to_string(index=False))
    
    # 5. Category Analysis
    print("\n5️⃣ TOP 10 CATEGORIES")
    print("-" * 50)
    
    category_query = """
    SELECT category, COUNT(*) as product_count
    FROM products 
    GROUP BY category 
    ORDER BY product_count DESC 
    LIMIT 10
    """
    category_data = pd.read_sql_query(category_query, conn)
    print(category_data.to_string(index=False))
    
    # 6. Sample Products by Department
    print("\n6️⃣ SAMPLE PRODUCTS BY DEPARTMENT")
    print("-" * 50)
    
    # Men's products
    men_query = """
    SELECT id, name, brand, retail_price, category 
    FROM products 
    WHERE department = 'Men'
    ORDER BY RANDOM() 
    LIMIT 3
    """
    men_data = pd.read_sql_query(men_query, conn)
    print("👔 MEN'S PRODUCTS:")
    for _, row in men_data.iterrows():
        print(f"   ID: {row['id']}, Name: {row['name'][:60]}..., Brand: {row['brand']}, Price: ${row['retail_price']:.2f}")
    
    print("\n👗 WOMEN'S PRODUCTS:")
    women_query = """
    SELECT id, name, brand, retail_price, category 
    FROM products 
    WHERE department = 'Women'
    ORDER BY RANDOM() 
    LIMIT 3
    """
    women_data = pd.read_sql_query(women_query, conn)
    for _, row in women_data.iterrows():
        print(f"   ID: {row['id']}, Name: {row['name'][:60]}..., Brand: {row['brand']}, Price: ${row['retail_price']:.2f}")
    
    # 7. Price Range Analysis
    print("\n7️⃣ PRICE RANGE ANALYSIS")
    print("-" * 50)
    
    price_range_query = """
    SELECT 
        CASE 
            WHEN retail_price < 10 THEN 'Under $10'
            WHEN retail_price < 25 THEN '$10-$25'
            WHEN retail_price < 50 THEN '$25-$50'
            WHEN retail_price < 100 THEN '$50-$100'
            ELSE 'Over $100'
        END as price_range,
        COUNT(*) as product_count
    FROM products 
    GROUP BY price_range
    ORDER BY MIN(retail_price)
    """
    price_range_data = pd.read_sql_query(price_range_query, conn)
    print(price_range_data.to_string(index=False))
    
    # 8. Data Quality Check
    print("\n8️⃣ DATA QUALITY CHECK")
    print("-" * 50)
    
    quality_query = """
    SELECT 
        'Total Products' as check_type,
        COUNT(*) as count
    FROM products
    UNION ALL
    SELECT 
        'Products with valid prices' as check_type,
        COUNT(*) as count
    FROM products
    WHERE cost >= 0 AND retail_price >= 0
    UNION ALL
    SELECT 
        'Products with valid departments' as check_type,
        COUNT(*) as count
    FROM products
    WHERE department IN ('Men', 'Women')
    UNION ALL
    SELECT 
        'Products with valid SKU length' as check_type,
        COUNT(*) as count
    FROM products
    WHERE length(sku) = 32
    """
    quality_data = pd.read_sql_query(quality_query, conn)
    print(quality_data.to_string(index=False))
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ ALL QUERIES EXECUTED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    detailed_query_demo() 