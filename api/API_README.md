# 🚀 E-commerce Products REST API

A Flask-based REST API for accessing product data from the SQLite database.

## 📋 Features

- ✅ **RESTful Design**: Standard HTTP methods and status codes
- ✅ **Pagination**: Efficient handling of large datasets
- ✅ **Search Functionality**: Search by name, brand, or category
- ✅ **Filtering**: Filter by category or department
- ✅ **Error Handling**: Proper HTTP status codes and error messages
- ✅ **CORS Support**: Ready for frontend integration
- ✅ **Health Check**: API status monitoring
- ✅ **Statistics**: Database statistics endpoint

## 🛠️ Installation

1. **Install Dependencies:**
   ```bash
   pip install -r api_requirements.txt
   ```

2. **Start the API Server:**
   ```bash
   python app.py
   ```

3. **API will be available at:** `http://localhost:5000`

## 📚 API Endpoints

### 1. **GET /api/products** - List All Products
**Description:** Get all products with pagination

**Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10, max: 100)

**Example:**
```bash
curl "http://localhost:5000/api/products?page=1&per_page=5"
```

**Response:**
```json
{
  "products": [
    {
      "id": 13842,
      "name": "Low Profile Dyed Cotton Twill Cap - Navy W39S55D",
      "brand": "MG",
      "retail_price": 6.25,
      "cost": 2.52,
      "category": "Accessories",
      "department": "Women",
      "sku": "EBD58B8A3F1D72F4206201DA62FB1204",
      "distribution_center_id": 1
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 5,
    "total_count": 29120,
    "total_pages": 5824,
    "has_next": true,
    "has_prev": false
  }
}
```

### 2. **GET /api/products/{id}** - Get Specific Product
**Description:** Get a product by its ID

**Example:**
```bash
curl "http://localhost:5000/api/products/13842"
```

**Response:**
```json
{
  "id": 13842,
  "name": "Low Profile Dyed Cotton Twill Cap - Navy W39S55D",
  "brand": "MG",
  "retail_price": 6.25,
  "cost": 2.52,
  "category": "Accessories",
  "department": "Women",
  "sku": "EBD58B8A3F1D72F4206201DA62FB1204",
  "distribution_center_id": 1
}
```

### 3. **GET /api/products/search?q={query}** - Search Products
**Description:** Search products by name, brand, or category

**Example:**
```bash
curl "http://localhost:5000/api/products/search?q=jeans"
```

**Response:**
```json
{
  "products": [...],
  "query": "jeans",
  "count": 15
}
```

### 4. **GET /api/products/category/{category}** - Get Products by Category
**Description:** Get products filtered by category

**Example:**
```bash
curl "http://localhost:5000/api/products/category/Jeans"
```

**Response:**
```json
{
  "products": [...],
  "category": "Jeans",
  "count": 1999
}
```

### 5. **GET /api/products/department/{department}** - Get Products by Department
**Description:** Get products filtered by department (Men/Women)

**Example:**
```bash
curl "http://localhost:5000/api/products/department/Men"
```

**Response:**
```json
{
  "products": [...],
  "department": "Men",
  "count": 13131
}
```

### 6. **GET /api/stats** - Get Database Statistics
**Description:** Get comprehensive database statistics

**Example:**
```bash
curl "http://localhost:5000/api/stats"
```

**Response:**
```json
{
  "total_products": 29120,
  "total_categories": 26,
  "total_brands": 2757,
  "departments": [
    {"department": "Women", "count": 15989},
    {"department": "Men", "count": 13131}
  ],
  "price_stats": {
    "min_price": 0.02,
    "max_price": 999.0,
    "avg_price": 59.22
  }
}
```

### 7. **GET /api/health** - Health Check
**Description:** Check API and database status

**Example:**
```bash
curl "http://localhost:5000/api/health"
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "total_products": 29120,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 🔧 HTTP Status Codes

- **200 OK**: Request successful
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Product not found
- **500 Internal Server Error**: Server error

## 🧪 Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

**Prerequisites:**
- API server must be running (`python app.py`)
- Install requests: `pip install requests`

## 📊 Database Schema

The API connects to the `ecommerce_improved.db` SQLite database with the following schema:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    cost REAL NOT NULL CHECK (cost >= 0),
    category TEXT NOT NULL CHECK (length(category) <= 50),
    name TEXT CHECK (length(name) <= 500),
    brand TEXT CHECK (length(brand) <= 100),
    retail_price REAL NOT NULL CHECK (retail_price >= 0),
    department TEXT NOT NULL CHECK (department IN ('Men', 'Women')),
    sku TEXT NOT NULL CHECK (length(sku) = 32) UNIQUE,
    distribution_center_id INTEGER NOT NULL CHECK (distribution_center_id BETWEEN 1 AND 10)
);
```

## 🚀 Usage Examples

### Using curl:
```bash
# Get first 10 products
curl "http://localhost:5000/api/products"

# Get specific product
curl "http://localhost:5000/api/products/13842"

# Search for jeans
curl "http://localhost:5000/api/products/search?q=jeans"

# Get men's products
curl "http://localhost:5000/api/products/department/Men"

# Get statistics
curl "http://localhost:5000/api/stats"
```

### Using JavaScript (Frontend):
```javascript
// Get products
fetch('http://localhost:5000/api/products?page=1&per_page=10')
  .then(response => response.json())
  .then(data => console.log(data));

// Search products
fetch('http://localhost:5000/api/products/search?q=shirt')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔒 Security Features

- **Input Validation**: All parameters are validated
- **SQL Injection Protection**: Parameterized queries
- **CORS Headers**: Configured for frontend integration
- **Error Handling**: Comprehensive error responses

## 📈 Performance Features

- **Pagination**: Efficient handling of large datasets
- **Database Indexes**: Optimized queries
- **Connection Pooling**: Efficient database connections
- **Response Caching**: Built-in Flask caching

## 🎯 Key Benefits

1. **RESTful Design**: Standard HTTP conventions
2. **Comprehensive API**: All CRUD operations covered
3. **Production Ready**: Error handling and validation
4. **Frontend Ready**: CORS enabled for web applications
5. **Scalable**: Pagination and efficient queries
6. **Well Documented**: Clear endpoint documentation

## 📝 Files Structure

```
database_setup/
├── app.py                    # Main Flask API application
├── test_api.py              # API testing script
├── api_requirements.txt     # Python dependencies
├── API_README.md           # This documentation
└── ecommerce_improved.db   # SQLite database
```

**Status**: ✅ **REST API ready for production use!** 