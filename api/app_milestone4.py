import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('ecommerce_improved.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM products')
        product_count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'ecommerce_improved.db',
            'products_count': product_count
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/products')
def get_products():
    """Get all products with pagination and department info"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM products')
        total_products = cursor.fetchone()[0]
        
        # Get products with department info
        cursor.execute('''
            SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price, 
                   p.sku, p.distribution_center_id, d.name as department
            FROM products p
            JOIN departments d ON p.department_id = d.id
            ORDER BY p.id
            LIMIT ? OFFSET ?
        ''', (per_page, offset))
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'cost': row['cost'],
                'category': row['category'],
                'name': row['name'],
                'brand': row['brand'],
                'retail_price': row['retail_price'],
                'sku': row['sku'],
                'distribution_center_id': row['distribution_center_id'],
                'department': row['department']
            })
        
        conn.close()
        
        total_pages = (total_products + per_page - 1) // per_page
        
        return jsonify({
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_products': total_products,
                'total_pages': total_pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    """Get a specific product by ID with department info"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price, 
                   p.sku, p.distribution_center_id, d.name as department
            FROM products p
            JOIN departments d ON p.department_id = d.id
            WHERE p.id = ?
        ''', (product_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            product = {
                'id': row['id'],
                'cost': row['cost'],
                'category': row['category'],
                'name': row['name'],
                'brand': row['brand'],
                'retail_price': row['retail_price'],
                'sku': row['sku'],
                'distribution_center_id': row['distribution_center_id'],
                'department': row['department']
            }
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/search')
def search_products():
    """Search products with department info"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price, 
                   p.sku, p.distribution_center_id, d.name as department
            FROM products p
            JOIN departments d ON p.department_id = d.id
            WHERE p.name LIKE ? OR p.brand LIKE ? OR p.category LIKE ?
            ORDER BY p.name
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'cost': row['cost'],
                'category': row['category'],
                'name': row['name'],
                'brand': row['brand'],
                'retail_price': row['retail_price'],
                'sku': row['sku'],
                'distribution_center_id': row['distribution_center_id'],
                'department': row['department']
            })
        
        conn.close()
        
        return jsonify({
            'products': products,
            'count': len(products),
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/department/<department_name>')
def get_products_by_department(department_name):
    """Get products by department name"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price, 
                   p.sku, p.distribution_center_id, d.name as department
            FROM products p
            JOIN departments d ON p.department_id = d.id
            WHERE d.name = ?
            ORDER BY p.name
        ''', (department_name,))
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'cost': row['cost'],
                'category': row['category'],
                'name': row['name'],
                'brand': row['brand'],
                'retail_price': row['retail_price'],
                'sku': row['sku'],
                'distribution_center_id': row['distribution_center_id'],
                'department': row['department']
            })
        
        conn.close()
        
        return jsonify({
            'products': products,
            'count': len(products),
            'department': department_name
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/departments')
def get_departments():
    """Get all departments"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, created_at, updated_at FROM departments ORDER BY id')
        
        departments = []
        for row in cursor.fetchall():
            departments.append({
                'id': row['id'],
                'name': row['name'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
        
        conn.close()
        
        return jsonify({
            'departments': departments,
            'count': len(departments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """Get database statistics with department info"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total products
        cursor.execute('SELECT COUNT(*) FROM products')
        total_products = cursor.fetchone()[0]
        
        # Total categories
        cursor.execute('SELECT COUNT(DISTINCT category) FROM products')
        total_categories = cursor.fetchone()[0]
        
        # Total brands
        cursor.execute('SELECT COUNT(DISTINCT brand) FROM products')
        total_brands = cursor.fetchone()[0]
        
        # Total departments
        cursor.execute('SELECT COUNT(*) FROM departments')
        total_departments = cursor.fetchone()[0]
        
        # Price statistics
        cursor.execute('''
            SELECT 
                AVG(retail_price) as avg_price,
                MIN(retail_price) as min_price,
                MAX(retail_price) as max_price
            FROM products
        ''')
        price_stats = cursor.fetchone()
        
        # Department breakdown
        cursor.execute('''
            SELECT d.name, COUNT(p.id) as product_count
            FROM departments d
            LEFT JOIN products p ON d.id = p.department_id
            GROUP BY d.id, d.name
            ORDER BY d.id
        ''')
        
        department_breakdown = []
        for row in cursor.fetchall():
            department_breakdown.append({
                'name': row[0],
                'product_count': row[1]
            })
        
        conn.close()
        
        return jsonify({
            'total_products': total_products,
            'total_categories': total_categories,
            'total_brands': total_brands,
            'total_departments': total_departments,
            'price_stats': {
                'avg_price': round(price_stats[0], 2) if price_stats[0] else 0,
                'min_price': price_stats[1] if price_stats[1] else 0,
                'max_price': price_stats[2] if price_stats[2] else 0
            },
            'department_breakdown': department_breakdown
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting E-commerce Products API (Milestone 4 - Department Refactored)...")
    print("📊 Database: ecommerce_improved.db")
    print("🌐 API will be available at: http://localhost:5000")
    print("📋 Available endpoints:")
    print("   GET /api/products - List all products (with pagination)")
    print("   GET /api/products/{id} - Get specific product")
    print("   GET /api/products/search?q=query - Search products")
    print("   GET /api/products/department/{department} - Get products by department")
    print("   GET /api/departments - Get all departments")
    print("   GET /api/stats - Get database statistics")
    print("   GET /api/health - Health check")
    print()
    print("✅ API is ready! Press Ctrl+C to stop.")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 