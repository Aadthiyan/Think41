# E-commerce Database Project

## Milestone 1: Database Design and Loading Data

This project sets up a database for an e-commerce dataset and loads product data from CSV files.

### Project Structure

```
database_setup/
├── database_setup.py              # Basic database setup script
├── improved_database_setup.py     # Improved database setup with validation
├── analyze_csv_structure.py       # CSV analysis script
├── query_database.py              # Database query examples
├── show_schema.py                 # Schema display script
├── check_git_files.py            # Git file checker
├── requirements.txt               # Python dependencies
├── README.md                     # This documentation file
└── .gitignore                    # Git ignore rules

archive/ (external data folder)
├── products.csv                   # Product data
├── orders.csv                    # Order data
├── order_items.csv               # Order items data
├── users.csv                     # User data
├── inventory_items.csv           # Inventory data
└── distribution_centers.csv      # Distribution centers data
```

### Database Schema

#### Products Table (Improved Design)

Based on thorough CSV analysis, the database schema includes:

- `id` (INTEGER PRIMARY KEY): Unique product identifier (1-29,120)
- `cost` (REAL NOT NULL): Product cost with CHECK constraint (≥ 0)
- `category` (TEXT NOT NULL): Product category with length constraint (≤ 50 chars)
- `name` (TEXT): Product name with length constraint (≤ 500 chars)
- `brand` (TEXT): Product brand with length constraint (≤ 100 chars)
- `retail_price` (REAL NOT NULL): Retail price with CHECK constraint (≥ 0)
- `department` (TEXT NOT NULL): Department with CHECK constraint ('Men' or 'Women')
- `sku` (TEXT NOT NULL UNIQUE): Stock keeping unit with exact length constraint (32 chars)
- `distribution_center_id` (INTEGER NOT NULL): Distribution center ID with range constraint (1-10)

#### Database Features

- **Data Validation**: CHECK constraints ensure data integrity
- **Performance Indexes**: Indexes on brand, category, department, and price
- **Data Cleaning**: Handles null values and validates data during import
- **Unique Constraints**: SKU uniqueness enforced

### Data Analysis Results

From the CSV analysis:
- **Total Products**: 29,120
- **Categories**: 26 unique categories
- **Brands**: 2,757 unique brands
- **Departments**: 2 (Men: 13,131, Women: 15,989)
- **Price Range**: $0.02 - $999.00 (avg: $59.22)
- **Cost Range**: $0.01 - $557.15 (avg: $28.48)
- **Data Quality**: ✅ No major issues found

### Setup Instructions

1. Navigate to the database_setup folder:
   ```bash
   cd database_setup
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the basic database setup:
   ```bash
   python database_setup.py
   ```

4. Run the improved database setup (recommended):
   ```bash
   python improved_database_setup.py
   ```

5. Analyze CSV structure:
   ```bash
   python analyze_csv_structure.py
   ```

### Verification Scripts

- `query_database.py` - Basic database queries
- `show_schema.py` - Display database schema
- `analyze_csv_structure.py` - Detailed CSV analysis

### Files Created

- `ecommerce.db`: Basic SQLite database file
- `ecommerce_improved.db`: Improved SQLite database with constraints

### Key Improvements

1. **Data Type Optimization**: Appropriate constraints based on actual data analysis
2. **Data Validation**: CHECK constraints prevent invalid data
3. **Performance**: Strategic indexes for common queries
4. **Data Cleaning**: Handles null values and validates during import
5. **Documentation**: Comprehensive analysis and schema documentation

### Git Repository

All files in this folder are ready to be pushed to GitHub. The `.gitignore` file ensures that:
- Database files (*.db) are excluded
- Data files (archive/) are excluded
- Only code and documentation are included

### Usage Examples

```bash
# Check which files will be pushed to GitHub
python check_git_files.py

# Initialize git repository
git init
git add .
git commit -m "Initial commit: E-commerce database setup"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
``` 