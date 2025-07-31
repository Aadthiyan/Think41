import requests
import json
import time

def demo_api_endpoints():
    """Demonstrate API endpoints with sample requests"""
    
    print("🚀 E-commerce Products API Demonstration")
    print("=" * 50)
    print("📋 Available Endpoints:")
    print("   GET /api/products - List all products (with pagination)")
    print("   GET /api/products/{id} - Get specific product")
    print("   GET /api/products/search?q=query - Search products")
    print("   GET /api/products/category/{category} - Get products by category")
    print("   GET /api/products/department/{department} - Get products by department")
    print("   GET /api/stats - Get database statistics")
    print("   GET /api/health - Health check")
    print("\n" + "=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Wait for server to be ready
    print("⏳ Waiting for API server to be ready...")
    time.sleep(3)
    
    # Test 1: Health Check
    print("\n1️⃣ Health Check Endpoint")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Database: {data['database']}")
            print(f"✅ Total Products: {data['total_products']}")
            print(f"✅ Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get Products (Paginated)
    print("\n2️⃣ Get Products Endpoint (Paginated)")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/products?page=1&per_page=3", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Products returned: {len(data['products'])}")
            print(f"✅ Total count: {data['pagination']['total_count']}")
            print(f"✅ Page: {data['pagination']['page']}/{data['pagination']['total_pages']}")
            
            # Show sample products
            for i, product in enumerate(data['products'], 1):
                print(f"   Product {i}:")
                print(f"     ID: {product['id']}")
                print(f"     Name: {product['name'][:50]}...")
                print(f"     Brand: {product['brand']}")
                print(f"     Price: ${product['retail_price']:.2f}")
                print(f"     Category: {product['category']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get Specific Product
    print("\n3️⃣ Get Specific Product Endpoint")
    print("-" * 35)
    try:
        response = requests.get(f"{base_url}/api/products/13842", timeout=10)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product found:")
            print(f"   ID: {product['id']}")
            print(f"   Name: {product['name']}")
            print(f"   Brand: {product['brand']}")
            print(f"   Price: ${product['retail_price']:.2f}")
            print(f"   Cost: ${product['cost']:.2f}")
            print(f"   Category: {product['category']}")
            print(f"   Department: {product['department']}")
            print(f"   SKU: {product['sku']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Search Products
    print("\n4️⃣ Search Products Endpoint")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/api/products/search?q=jeans", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search results for 'jeans': {data['count']} products")
            if data['products']:
                print("   Sample results:")
                for i, product in enumerate(data['products'][:3], 1):
                    print(f"     {i}. {product['name'][:60]}...")
                    print(f"        Brand: {product['brand']}, Price: ${product['retail_price']:.2f}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Get Products by Category
    print("\n5️⃣ Get Products by Category Endpoint")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/products/category/Jeans", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Jeans category: {data['count']} products")
            if data['products']:
                print("   Sample products:")
                for i, product in enumerate(data['products'][:3], 1):
                    print(f"     {i}. {product['name'][:50]}...")
                    print(f"        Brand: {product['brand']}, Price: ${product['retail_price']:.2f}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Get Products by Department
    print("\n6️⃣ Get Products by Department Endpoint")
    print("-" * 42)
    try:
        response = requests.get(f"{base_url}/api/products/department/Men", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Men's department: {data['count']} products")
            if data['products']:
                print("   Sample products:")
                for i, product in enumerate(data['products'][:3], 1):
                    print(f"     {i}. {product['name'][:50]}...")
                    print(f"        Brand: {product['brand']}, Price: ${product['retail_price']:.2f}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Get Statistics
    print("\n7️⃣ Get Statistics Endpoint")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Database Statistics:")
            print(f"   Total Products: {stats['total_products']}")
            print(f"   Total Categories: {stats['total_categories']}")
            print(f"   Total Brands: {stats['total_brands']}")
            print(f"   Price Range: ${stats['price_stats']['min_price']:.2f} - ${stats['price_stats']['max_price']:.2f}")
            print(f"   Average Price: ${stats['price_stats']['avg_price']:.2f}")
            print("   Department Distribution:")
            for dept in stats['departments']:
                print(f"     {dept['department']}: {dept['count']} products")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 8: Error Handling
    print("\n8️⃣ Error Handling Test")
    print("-" * 25)
    try:
        response = requests.get(f"{base_url}/api/products/999999", timeout=10)
        if response.status_code == 404:
            error_data = response.json()
            print(f"✅ Error handling working correctly:")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {error_data['error']}")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API Demonstration Complete!")
    print("=" * 50)

if __name__ == "__main__":
    print("⚠️  Make sure the API server is running!")
    print("   Start it with: python app.py")
    print("\nStarting demonstration in 3 seconds...")
    time.sleep(3)
    demo_api_endpoints() 