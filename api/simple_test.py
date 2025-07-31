import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Simple API Test")
    print("=" * 30)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Total Products: {data['total_products']}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")
    
    # Test 2: Get Products
    print("\n2. Testing Get Products...")
    try:
        response = requests.get(f"{base_url}/api/products?page=1&per_page=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get Products: {len(data['products'])} products returned")
            print(f"   Total Count: {data['pagination']['total_count']}")
            
            # Show first product
            if data['products']:
                first_product = data['products'][0]
                print(f"   Sample: ID {first_product['id']}, {first_product['name'][:40]}...")
        else:
            print(f"❌ Get Products failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Products error: {e}")
    
    # Test 3: Get Specific Product
    print("\n3. Testing Get Specific Product...")
    try:
        response = requests.get(f"{base_url}/api/products/13842")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Get Product: ID {product['id']}")
            print(f"   Name: {product['name'][:40]}...")
            print(f"   Brand: {product['brand']}")
            print(f"   Price: ${product['retail_price']:.2f}")
        else:
            print(f"❌ Get Product failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Product error: {e}")
    
    # Test 4: Search Products
    print("\n4. Testing Search Products...")
    try:
        response = requests.get(f"{base_url}/api/products/search?q=shirt")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search Products: {data['count']} results for 'shirt'")
            if data['products']:
                first_result = data['products'][0]
                print(f"   Sample: {first_result['name'][:40]}...")
        else:
            print(f"❌ Search Products failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search Products error: {e}")
    
    # Test 5: Get Stats
    print("\n5. Testing Get Statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics:")
            print(f"   Total Products: {stats['total_products']}")
            print(f"   Total Categories: {stats['total_categories']}")
            print(f"   Total Brands: {stats['total_brands']}")
        else:
            print(f"❌ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Statistics error: {e}")
    
    print("\n" + "=" * 30)
    print("🎯 Simple API Test Complete!")

if __name__ == "__main__":
    test_api() 