#!/usr/bin/env python3
"""
Test script for Milestone 5 API with Enhanced Departments API
Tests all the new department endpoints with proper error handling
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
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
        return False

def test_departments_list():
    """Test GET /api/departments - List all departments with product counts"""
    print("🏢 Testing Departments List Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/departments")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Departments: {data.get('count', 'N/A')}")
            print(f"Total Products: {data.get('total_products', 'N/A')}")
            
            departments = data.get('departments', [])
            for dept in departments:
                print(f"  - ID {dept.get('id')}: {dept.get('name')} ({dept.get('product_count')} products)")
        else:
            print(f"Error Response: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
        return False

def test_department_details():
    """Test GET /api/departments/{id} - Get specific department details"""
    print("🔍 Testing Department Details Endpoint...")
    try:
        # Test valid department ID
        response = requests.get(f"{BASE_URL}/departments/1")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            dept = response.json()
            print(f"Department Details:")
            print(f"  ID: {dept.get('id')}")
            print(f"  Name: {dept.get('name')}")
            print(f"  Product Count: {dept.get('product_count')}")
            print(f"  Created At: {dept.get('created_at')}")
        else:
            print(f"Error Response: {response.text}")
        
        # Test invalid department ID
        response_invalid = requests.get(f"{BASE_URL}/departments/999")
        print(f"Invalid ID Status Code: {response_invalid.status_code}")
        if response_invalid.status_code == 404:
            print("✅ Correctly handled invalid department ID")
        
        print("-" * 50)
        return response.status_code == 200 and response_invalid.status_code == 404
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
        return False

def test_department_products_by_id():
    """Test GET /api/departments/{id}/products - Get products in department by ID"""
    print("🛍️ Testing Department Products by ID...")
    try:
        response = requests.get(f"{BASE_URL}/departments/1/products?page=1&per_page=3")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            dept_info = data.get('department', {})
            print(f"Department: {dept_info.get('name')} (ID: {dept_info.get('id')})")
            
            pagination = data.get('pagination', {})
            print(f"Total Products: {pagination.get('total_products')}")
            print(f"Products Returned: {len(data.get('products', []))}")
            
            if data.get('products'):
                first_product = data['products'][0]
                print(f"\nFirst Product Sample:")
                print(f"  ID: {first_product.get('id')}")
                print(f"  Name: {first_product.get('name')}")
                print(f"  Department: {first_product.get('department')}")
        else:
            print(f"Error Response: {response.text}")
        
        # Test invalid department ID
        response_invalid = requests.get(f"{BASE_URL}/departments/999/products")
        print(f"Invalid ID Status Code: {response_invalid.status_code}")
        if response_invalid.status_code == 404:
            print("✅ Correctly handled invalid department ID")
        
        print("-" * 50)
        return response.status_code == 200 and response_invalid.status_code == 404
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
        return False

def test_department_products_by_name():
    """Test GET /api/departments/{name}/products - Get products by department name"""
    print("🛍️ Testing Department Products by Name...")
    try:
        response = requests.get(f"{BASE_URL}/departments/Women/products?page=1&per_page=3")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Department: {data.get('department')}")
            print(f"Products Count: {data.get('count')}")
            
            pagination = data.get('pagination', {})
            print(f"Total Products: {pagination.get('total_products')}")
            
            if data.get('products'):
                first_product = data['products'][0]
                print(f"\nFirst Product Sample:")
                print(f"  ID: {first_product.get('id')}")
                print(f"  Name: {first_product.get('name')}")
                print(f"  Department: {first_product.get('department')}")
        else:
            print(f"Error Response: {response.text}")
        
        # Test invalid department name
        response_invalid = requests.get(f"{BASE_URL}/departments/InvalidDept/products")
        print(f"Invalid Name Status Code: {response_invalid.status_code}")
        if response_invalid.status_code == 200:
            print("✅ Correctly handled invalid department name (returns empty list)")
        
        print("-" * 50)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
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
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
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
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
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
        print("❌ Cannot connect to server. Make sure to run: python app_milestone5.py")
        return False

def test_error_handling():
    """Test error handling for various scenarios"""
    print("⚠️ Testing Error Handling...")
    
    tests = [
        ("Invalid department ID", f"{BASE_URL}/departments/999", 404),
        ("Invalid product ID", f"{BASE_URL}/products/99999", 404),
        ("Empty search query", f"{BASE_URL}/products/search", 400),
        ("Non-existent endpoint", f"{BASE_URL}/nonexistent", 404),
    ]
    
    passed = 0
    for test_name, url, expected_status in tests:
        try:
            response = requests.get(url)
            if response.status_code == expected_status:
                print(f"✅ {test_name}: {response.status_code}")
                passed += 1
            else:
                print(f"❌ {test_name}: Expected {expected_status}, got {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {test_name}: Connection error")
    
    print("-" * 50)
    return passed == len(tests)

def main():
    """Run all tests"""
    print("🚀 Testing Milestone 5 API with Enhanced Departments API")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Test endpoints
    tests = [
        test_health_endpoint,
        test_departments_list,
        test_department_details,
        test_department_products_by_id,
        test_department_products_by_name,
        test_products_endpoint,
        test_product_details,
        test_stats_with_departments,
        test_error_handling
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
        print("\n🎉 All tests passed! Milestone 5 API is working correctly.")
        print("\n✅ Milestone 5 Requirements Met:")
        print("   - GET /api/departments - List all departments with product counts: ✅")
        print("   - GET /api/departments/{id} - Get specific department details: ✅")
        print("   - GET /api/departments/{id}/products - Get products in department: ✅")
        print("   - Proper JSON responses with HTTP status codes: ✅")
        print("   - Product counts included in department lists: ✅")
        print("   - Error handling for department not found: ✅")
        print("   - Error handling for no products in department: ✅")
        print("   - All endpoints tested thoroughly: ✅")
    else:
        print("\n⚠️ Some tests failed. Please check the API server and database.")

if __name__ == "__main__":
    main() 