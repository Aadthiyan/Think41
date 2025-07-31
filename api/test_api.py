import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing E-commerce Products API...")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Database: {data['database']}")
            print(f"   Total Products: {data['total_products']}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")
    
    # Test 2: Get All Products (first page)
    print("\n2️⃣ Testing Get All Products...")
    try:
        response = requests.get(f"{base_url}/api/products?page=1&per_page=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get Products: {len(data['products'])} products returned")
            print(f"   Total Count: {data['pagination']['total_count']}")
            print(f"   Page: {data['pagination']['page']}/{data['pagination']['total_pages']}")
            
            # Show first product
            if data['products']:
                first_product = data['products'][0]
                print(f"   Sample Product: ID {first_product['id']}, {first_product['name'][:50]}...")
        else:
            print(f"❌ Get Products failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Products error: {e}")
    
    # Test 3: Get Specific Product
    print("\n3️⃣ Testing Get Specific Product...")
    try:
        response = requests.get(f"{base_url}/api/products/13842")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Get Product: ID {product['id']}")
            print(f"   Name: {product['name'][:50]}...")
            print(f"   Brand: {product['brand']}")
            print(f"   Price: ${product['retail_price']:.2f}")
        else:
            print(f"❌ Get Product failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Product error: {e}")
    
    # Test 4: Search Products
    print("\n4️⃣ Testing Search Products...")
    try:
        response = requests.get(f"{base_url}/api/products/search?q=jeans")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search Products: {data['count']} results for 'jeans'")
            if data['products']:
                first_result = data['products'][0]
                print(f"   Sample Result: {first_result['name'][:50]}...")
        else:
            print(f"❌ Search Products failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search Products error: {e}")
    
    # Test 5: Get Products by Category
    print("\n5️⃣ Testing Get Products by Category...")
    try:
        response = requests.get(f"{base_url}/api/products/category/Jeans")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Category Products: {data['count']} jeans products")
            if data['products']:
                first_product = data['products'][0]
                print(f"   Sample: {first_product['name'][:50]}...")
        else:
            print(f"❌ Category Products failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Category Products error: {e}")
    
    # Test 6: Get Products by Department
    print("\n6️⃣ Testing Get Products by Department...")
    try:
        response = requests.get(f"{base_url}/api/products/department/Men")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Department Products: {data['count']} men's products")
            if data['products']:
                first_product = data['products'][0]
                print(f"   Sample: {first_product['name'][:50]}...")
        else:
            print(f"❌ Department Products failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Department Products error: {e}")
    
    # Test 7: Get Statistics
    print("\n7️⃣ Testing Get Statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics:")
            print(f"   Total Products: {stats['total_products']}")
            print(f"   Total Categories: {stats['total_categories']}")
            print(f"   Total Brands: {stats['total_brands']}")
            print(f"   Price Range: ${stats['price_stats']['min_price']:.2f} - ${stats['price_stats']['max_price']:.2f}")
        else:
            print(f"❌ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Statistics error: {e}")
    
    # Test 8: Error Handling
    print("\n8️⃣ Testing Error Handling...")
    try:
        # Test invalid product ID
        response = requests.get(f"{base_url}/api/products/999999")
        if response.status_code == 404:
            print("✅ Error Handling: Invalid product ID returns 404")
        else:
            print(f"❌ Error Handling: Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error Handling test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    print("⚠️  Make sure the API server is running on http://localhost:5000")
    print("   Run: python app.py")
    print("\nWaiting 3 seconds before testing...")
    time.sleep(3)
    test_api_endpoints() 