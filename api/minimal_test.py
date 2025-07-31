import sqlite3
import requests
import time

def test_database():
    """Test database connection"""
    print("🔍 Testing Database Connection...")
    try:
        conn = sqlite3.connect('ecommerce_improved.db')
        cursor = conn.cursor()
        
        # Test query
        cursor.execute('SELECT COUNT(*) FROM products')
        count = cursor.fetchone()[0]
        print(f"✅ Database connected! Total products: {count}")
        
        # Test sample product
        cursor.execute('SELECT id, name FROM products LIMIT 1')
        product = cursor.fetchone()
        print(f"✅ Sample product: ID {product[0]}, Name: {product[1][:50]}...")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_api_server():
    """Test if API server is running"""
    print("\n🌐 Testing API Server...")
    
    # Wait a bit for server to start
    time.sleep(2)
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Server running!")
            print(f"   Status: {data['status']}")
            print(f"   Products: {data['total_products']}")
            return True
        else:
            print(f"❌ API Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API Server not running on localhost:5000")
        print("   Please start the server with: python app.py")
        return False
    except Exception as e:
        print(f"❌ API Server error: {e}")
        return False

def main():
    print("🧪 Minimal API Test")
    print("=" * 40)
    
    # Test database
    db_ok = test_database()
    
    # Test API server
    api_ok = test_api_server()
    
    print("\n" + "=" * 40)
    if db_ok and api_ok:
        print("🎉 All tests passed! API is ready.")
    elif db_ok:
        print("⚠️  Database OK, but API server needs to be started.")
        print("   Run: python app.py")
    else:
        print("❌ Database connection failed.")
    
    print("=" * 40)

if __name__ == "__main__":
    main() 