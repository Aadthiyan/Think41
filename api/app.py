from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Database configuration
DATABASE = 'ecommerce_improved.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row object to dictionary"""
    return dict(zip(row.keys(), row))

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with pagination"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate parameters
        if page < 1:
            return jsonify({'error': 'Page number must be greater than 0'}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        
        # Get total count
        total_count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        
        # Get products with pagination
        products = conn.execute('''
            SELECT id, name, brand, retail_price, cost, category, department, sku, distribution_center_id
            FROM products 
            ORDER BY id 
            LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()
        
        # Convert to list of dictionaries
        products_list = [dict_from_row(product) for product in products]
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        
        conn.close()
        
        return jsonify({
            'products': products_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        conn = get_db_connection()
        
        product = conn.execute('''
            SELECT id, name, brand, retail_price, cost, category, department, sku, distribution_center_id
            FROM products 
            WHERE id = ?
        ''', (product_id,)).fetchone()
        
        conn.close()
        
        if product is None:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify(dict_from_row(product)), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search products by name, brand, or category"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        conn = get_db_connection()
        
        # Search in name, brand, and category
        products = conn.execute('''
            SELECT id, name, brand, retail_price, cost, category, department, sku, distribution_center_id
            FROM products 
            WHERE name LIKE ? OR brand LIKE ? OR category LIKE ?
            ORDER BY id 
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
        
        products_list = [dict_from_row(product) for product in products]
        
        conn.close()
        
        return jsonify({
            'products': products_list,
            'query': query,
            'count': len(products_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    try:
        conn = get_db_connection()
        
        products = conn.execute('''
            SELECT id, name, brand, retail_price, cost, category, department, sku, distribution_center_id
            FROM products 
            WHERE category = ?
            ORDER BY id 
            LIMIT 50
        ''', (category,)).fetchall()
        
        products_list = [dict_from_row(product) for product in products]
        
        conn.close()
        
        return jsonify({
            'products': products_list,
            'category': category,
            'count': len(products_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/products/department/<department>', methods=['GET'])
def get_products_by_department(department):
    """Get products by department (Men/Women)"""
    try:
        if department not in ['Men', 'Women']:
            return jsonify({'error': 'Department must be "Men" or "Women"'}), 400
        
        conn = get_db_connection()
        
        products = conn.execute('''
            SELECT id, name, brand, retail_price, cost, category, department, sku, distribution_center_id
            FROM products 
            WHERE department = ?
            ORDER BY id 
            LIMIT 50
        ''', (department,)).fetchall()
        
        products_list = [dict_from_row(product) for product in products]
        
        conn.close()
        
        return jsonify({
            'products': products_list,
            'department': department,
            'count': len(products_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        conn = get_db_connection()
        
        # Get basic stats
        total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        total_categories = conn.execute('SELECT COUNT(DISTINCT category) FROM products').fetchone()[0]
        total_brands = conn.execute('SELECT COUNT(DISTINCT brand) FROM products').fetchone()[0]
        
        # Get department stats
        dept_stats = conn.execute('''
            SELECT department, COUNT(*) as count
            FROM products 
            GROUP BY department
        ''').fetchall()
        
        # Get price stats
        price_stats = conn.execute('''
            SELECT 
                MIN(retail_price) as min_price,
                MAX(retail_price) as max_price,
                AVG(retail_price) as avg_price
            FROM products
        ''').fetchone()
        
        conn.close()
        
        return jsonify({
            'total_products': total_products,
            'total_categories': total_categories,
            'total_brands': total_brands,
            'departments': [dict_from_row(dept) for dept in dept_stats],
            'price_stats': {
                'min_price': price_stats[0],
                'max_price': price_stats[1],
                'avg_price': price_stats[2]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        product_count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'total_products': product_count,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting E-commerce Products API...")
    print("📊 Database:", DATABASE)
    print("🌐 API will be available at: http://localhost:5000")
    print("📋 Available endpoints:")
    print("   GET /api/products - List all products (with pagination)")
    print("   GET /api/products/{id} - Get specific product")
    print("   GET /api/products/search?q=query - Search products")
    print("   GET /api/products/category/{category} - Get products by category")
    print("   GET /api/products/department/{department} - Get products by department")
    print("   GET /api/stats - Get database statistics")
    print("   GET /api/health - Health check")
    print("\n✅ API is ready! Press Ctrl+C to stop.")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 