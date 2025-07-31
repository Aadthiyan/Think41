import sqlite3

def show_schema():
    """Display the database schema"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("=== Database Schema ===")
    
    # Get table information
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        print("-" * 50)
        
        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"{'Column Name':<20} {'Type':<15} {'Not Null':<10} {'Primary Key':<12}")
        print("-" * 60)
        
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"{name:<20} {type_name:<15} {'YES' if not_null else 'NO':<10} {'YES' if pk else 'NO':<12}")
    
    conn.close()

if __name__ == "__main__":
    show_schema() 