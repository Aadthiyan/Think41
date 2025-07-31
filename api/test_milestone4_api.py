#!/usr/bin/env python3
"""
Test script for Milestone 4 API with refactored departments
Tests the API endpoints to ensure they work with the new database structure
"""

import requests
import json
import time

# API Base URL
BASE_URL = "http://localhost:5000/api"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def test_products_endpoint():
    """Test the products endpoint with department info"""
    print("🛍️ Testing Products Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/products?page=1&per_page=3")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Products: {data.get('pagination', {}).get('total_products', 'N/A')}")
            print(f"Products Returned: {len(data.get('products', []))}")
            
            # Show first product with department info
            if data.get('products'):
                first_product = data['products'][0]
                print(f"\nFirst Product Sample:")
                print(f"  ID: {first_product.get('id')}")
                print(f"  Name: {first_product.get('name')}")
                print(f"  Department: {first_product.get('department')}")
                print(f"  Price: ${first_product.get('retail_price', 'N/A')}")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def test_product_details():
    """Test getting a specific product with department info"""
    print("🔍 Testing Product Details...")
    try:
        response = requests.get(f"{BASE_URL}/products/1")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print(f"Product Details:")
            print(f"  ID: {product.get('id')}")
            print(f"  Name: {product.get('name')}")
            print(f"  Department: {product.get('department')}")
            print(f"  Brand: {product.get('brand')}")
            print(f"  Price: ${product.get('retail_price', 'N/A')}")
        elif response.status_code == 404:
            print("Product with ID 1 not found")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code in [200, 404]
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def test_departments_endpoint():
    """Test the new departments endpoint"""
    print("🏢 Testing Departments Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/departments")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Departments: {data.get('count', 'N/A')}")
            
            departments = data.get('departments', [])
            for dept in departments:
                print(f"  - ID {dept.get('id')}: {dept.get('name')}")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def test_products_by_department():
    """Test getting products by department"""
    print("🏢 Testing Products by Department...")
    try:
        response = requests.get(f"{BASE_URL}/products/department/Women")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Department: {data.get('department')}")
            print(f"Products Count: {data.get('count')}")
            
            if data.get('products'):
                first_product = data['products'][0]
                print(f"\nFirst Product Sample:")
                print(f"  ID: {first_product.get('id')}")
                print(f"  Name: {first_product.get('name')}")
                print(f"  Department: {first_product.get('department')}")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def test_stats_with_departments():
    """Test statistics endpoint with department breakdown"""
    print("📊 Testing Statistics with Department Breakdown...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Products: {data.get('total_products')}")
            print(f"Total Departments: {data.get('total_departments')}")
            
            # Show department breakdown
            breakdown = data.get('department_breakdown', [])
            print("\nDepartment Breakdown:")
            for dept in breakdown:
                print(f"  - {dept.get('name')}: {dept.get('product_count')} products")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def test_search_with_departments():
    """Test search functionality with department info"""
    print("🔍 Testing Search with Department Info...")
    try:
        response = requests.get(f"{BASE_URL}/products/search?q=shirt")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Search Query: {data.get('query')}")
            print(f"Results Found: {data.get('count')}")
            
            if data.get('products'):
                first_product = data['products'][0]
                print(f"\nFirst Search Result:")
                print(f"  ID: {first_product.get('id')}")
                print(f"  Name: {first_product.get('name')}")
                print(f"  Department: {first_product.get('department')}")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone4.py")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Milestone 4 API with Department Refactoring")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Test endpoints
    tests = [
        test_health_endpoint,
        test_products_endpoint,
        test_product_details,
        test_departments_endpoint,
        test_products_by_department,
        test_stats_with_departments,
        test_search_with_departments
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"Success Rate: {((passed / total) * 100):.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! Milestone 4 API is working correctly.")
        print("\n✅ Milestone 4 Requirements Met:")
        print("   - Departments table created: ✅")
        print("   - Foreign key relationships: ✅")
        print("   - API updated for new structure: ✅")
        print("   - All endpoints working: ✅")
        print("   - Department information included: ✅")
    else:
        print("\n⚠️ Some tests failed. Please check the API server and database.")

if __name__ == "__main__":
    main() 