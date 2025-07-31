import requests
import json
import time

def quick_api_test():
    """Quick test of API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Quick API Test")
    print("=" * 30)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"   Total Products: {data['total_products']}")
        else:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get Products
    print("\n2. Testing Get Products...")
    try:
        response = requests.get(f"{base_url}/api/products?page=1&per_page=3")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get Products: {len(data['products'])} products returned")
            print(f"   Total Count: {data['pagination']['total_count']}")
            
            # Show first product
            if data['products']:
                first_product = data['products'][0]
                print(f"   Sample: ID {first_product['id']}, {first_product['name'][:40]}...")
        else:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get Specific Product
    print("\n3. Testing Get Specific Product...")
    try:
        response = requests.get(f"{base_url}/api/products/13842")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Get Product: ID {product['id']}")
            print(f"   Name: {product['name'][:40]}...")
        else:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 30)
    print("🎯 Quick Test Complete!")

if __name__ == "__main__":
    quick_api_test() 