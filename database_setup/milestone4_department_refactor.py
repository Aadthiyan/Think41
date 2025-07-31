#!/usr/bin/env python3
"""
Milestone 4: Department Refactoring Script
Refactor the database to move departments into a separate table with proper foreign key relationships.
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

class DepartmentRefactor:
    def __init__(self, db_path='ecommerce_improved.db'):
        self.db_path = db_path
        self.backup_path = f'ecommerce_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        
    def create_backup(self):
        """Create a backup of the current database"""
        print("🔄 Creating database backup...")
        try:
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✅ Backup created: {self.backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def show_current_schema(self):
        """Display the current database schema"""
        print("\n📋 Current Database Schema:")
        print("=" * 50)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            print("-" * 30)
            
            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, name, type_name, not_null, default_val, pk = col
                constraints = []
                if not_null:
                    constraints.append("NOT NULL")
                if pk:
                    constraints.append("PRIMARY KEY")
                if default_val:
                    constraints.append(f"DEFAULT {default_val}")
                
                constraint_str = " ".join(constraints)
                print(f"  {name:<20} {type_name:<15} {constraint_str}")
        
        conn.close()
    
    def create_departments_table(self):
        """Create the new departments table"""
        print("\n🏗️ Creating departments table...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Create departments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE CHECK (name IN ('Men', 'Women')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for department name
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_departments_name ON departments(name)')
            
            conn.commit()
            print("✅ Departments table created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating departments table: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def extract_unique_departments(self):
        """Extract unique department names from products table"""
        print("\n🔍 Extracting unique departments from products...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get unique departments
            cursor.execute('SELECT DISTINCT department FROM products WHERE department IS NOT NULL')
            departments = cursor.fetchall()
            
            unique_departments = [dept[0] for dept in departments if dept[0]]
            print(f"✅ Found {len(unique_departments)} unique departments: {unique_departments}")
            
            return unique_departments
            
        except Exception as e:
            print(f"❌ Error extracting departments: {e}")
            return []
        finally:
            conn.close()
    
    def populate_departments_table(self, departments):
        """Populate the departments table with unique departments"""
        print("\n📝 Populating departments table...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for dept in departments:
                cursor.execute('''
                    INSERT OR IGNORE INTO departments (name) 
                    VALUES (?)
                ''', (dept,))
            
            conn.commit()
            
            # Verify insertion
            cursor.execute('SELECT COUNT(*) FROM departments')
            count = cursor.fetchone()[0]
            print(f"✅ Departments table populated with {count} departments")
            
            # Show departments
            cursor.execute('SELECT id, name FROM departments ORDER BY id')
            dept_list = cursor.fetchall()
            for dept_id, dept_name in dept_list:
                print(f"  - ID {dept_id}: {dept_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error populating departments: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def update_products_table(self):
        """Update products table to use foreign key relationship"""
        print("\n🔄 Updating products table with foreign key...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # First, create a temporary table with the new structure
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products_new (
                    id INTEGER PRIMARY KEY,
                    cost REAL NOT NULL CHECK (cost >= 0),
                    category TEXT NOT NULL CHECK (length(category) <= 50),
                    name TEXT CHECK (length(name) <= 500),
                    brand TEXT CHECK (length(brand) <= 100),
                    retail_price REAL NOT NULL CHECK (retail_price >= 0),
                    department_id INTEGER NOT NULL,
                    sku TEXT NOT NULL CHECK (length(sku) = 32) UNIQUE,
                    distribution_center_id INTEGER NOT NULL CHECK (distribution_center_id BETWEEN 1 AND 10),
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                )
            ''')
            
            # Copy data from old table to new table with department_id mapping
            cursor.execute('''
                INSERT INTO products_new (id, cost, category, name, brand, retail_price, department_id, sku, distribution_center_id)
                SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price, d.id, p.sku, p.distribution_center_id
                FROM products p
                JOIN departments d ON p.department = d.name
            ''')
            
            # Drop the old table
            cursor.execute('DROP TABLE products')
            
            # Rename new table to products
            cursor.execute('ALTER TABLE products_new RENAME TO products')
            
            # Recreate indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_department_id ON products(department_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_price ON products(retail_price)')
            
            conn.commit()
            print("✅ Products table updated with foreign key relationship!")
            return True
            
        except Exception as e:
            print(f"❌ Error updating products table: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def verify_refactoring(self):
        """Verify the refactoring was successful"""
        print("\n🔍 Verifying refactoring...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check departments table
            cursor.execute('SELECT COUNT(*) FROM departments')
            dept_count = cursor.fetchone()[0]
            print(f"✅ Departments table: {dept_count} departments")
            
            # Check products table
            cursor.execute('SELECT COUNT(*) FROM products')
            product_count = cursor.fetchone()[0]
            print(f"✅ Products table: {product_count} products")
            
            # Check foreign key relationships
            cursor.execute('''
                SELECT COUNT(*) FROM products p
                JOIN departments d ON p.department_id = d.id
            ''')
            valid_relationships = cursor.fetchone()[0]
            print(f"✅ Valid foreign key relationships: {valid_relationships}")
            
            # Show sample data
            print("\n📊 Sample Data:")
            cursor.execute('''
                SELECT p.id, p.name, p.brand, d.name as department, p.retail_price
                FROM products p
                JOIN departments d ON p.department_id = d.id
                LIMIT 5
            ''')
            
            sample_data = cursor.fetchall()
            for row in sample_data:
                print(f"  - ID {row[0]}: {row[1]} ({row[2]}) - {row[3]} - ${row[4]:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying refactoring: {e}")
            return False
        finally:
            conn.close()
    
    def run_migration(self):
        """Run the complete migration process"""
        print("🚀 Starting Milestone 4: Department Refactoring")
        print("=" * 60)
        
        # Step 1: Create backup
        if not self.create_backup():
            print("❌ Migration failed: Could not create backup")
            return False
        
        # Step 2: Show current schema
        self.show_current_schema()
        
        # Step 3: Create departments table
        if not self.create_departments_table():
            print("❌ Migration failed: Could not create departments table")
            return False
        
        # Step 4: Extract unique departments
        departments = self.extract_unique_departments()
        if not departments:
            print("❌ Migration failed: No departments found")
            return False
        
        # Step 5: Populate departments table
        if not self.populate_departments_table(departments):
            print("❌ Migration failed: Could not populate departments table")
            return False
        
        # Step 6: Update products table
        if not self.update_products_table():
            print("❌ Migration failed: Could not update products table")
            return False
        
        # Step 7: Verify refactoring
        if not self.verify_refactoring():
            print("❌ Migration failed: Verification failed")
            return False
        
        print("\n🎉 Milestone 4 Migration Completed Successfully!")
        print("=" * 60)
        print("✅ Database refactored with departments table")
        print("✅ Foreign key relationships established")
        print("✅ Backup created for safety")
        print("\n📋 Next Steps:")
        print("1. Test the new API")
        print("2. Update frontend if needed")
        print("3. Commit changes to Git")
        print("4. Inform Kiran about completion")
        
        return True

def main():
    """Main function to run the migration"""
    refactor = DepartmentRefactor()
    success = refactor.run_migration()
    
    if success:
        print("\n🏆 Milestone 4: Department Refactoring - COMPLETED!")
    else:
        print("\n❌ Milestone 4: Department Refactoring - FAILED!")

if __name__ == "__main__":
    main() 