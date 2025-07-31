import pandas as pd
import numpy as np
from pathlib import Path

def analyze_csv_structure():
    """Analyze the CSV structure to determine optimal data types"""
    csv_path = Path('archive/products.csv')
    
    print("=== CSV Structure Analysis ===")
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    print("\n=== Column Analysis ===")
    
    for column in df.columns:
        print(f"\n--- {column} ---")
        
        # Basic info
        print(f"Data type: {df[column].dtype}")
        print(f"Null values: {df[column].isnull().sum()}")
        print(f"Unique values: {df[column].nunique()}")
        
        # Sample values
        sample_values = df[column].dropna().head(3).tolist()
        print(f"Sample values: {sample_values}")
        
        # For numeric columns, show range
        if pd.api.types.is_numeric_dtype(df[column]):
            print(f"Min: {df[column].min()}")
            print(f"Max: {df[column].max()}")
            print(f"Mean: {df[column].mean():.2f}")
        
        # For text columns, show length statistics
        if pd.api.types.is_string_dtype(df[column]):
            lengths = df[column].astype(str).str.len()
            print(f"Min length: {lengths.min()}")
            print(f"Max length: {lengths.max()}")
            print(f"Avg length: {lengths.mean():.2f}")
    
    print("\n=== Data Type Recommendations ===")
    
    recommendations = {
        'id': 'INTEGER PRIMARY KEY',
        'cost': 'REAL (DECIMAL(10,2) for precision)',
        'category': 'TEXT (VARCHAR(50) would be sufficient)',
        'name': 'TEXT (VARCHAR(255) would be sufficient)',
        'brand': 'TEXT (VARCHAR(100) would be sufficient)',
        'retail_price': 'REAL (DECIMAL(10,2) for precision)',
        'department': 'TEXT (VARCHAR(20) would be sufficient)',
        'sku': 'TEXT (VARCHAR(100) would be sufficient)',
        'distribution_center_id': 'INTEGER'
    }
    
    for col, recommendation in recommendations.items():
        print(f"{col}: {recommendation}")
    
    print("\n=== Potential Issues ===")
    
    # Check for potential issues
    issues = []
    
    # Check for duplicate IDs
    if df['id'].duplicated().any():
        issues.append("Duplicate IDs found")
    
    # Check for negative prices
    if (df['cost'] < 0).any() or (df['retail_price'] < 0).any():
        issues.append("Negative prices found")
    
    # Check for empty strings
    text_columns = ['category', 'name', 'brand', 'department', 'sku']
    for col in text_columns:
        if (df[col] == '').any():
            issues.append(f"Empty strings found in {col}")
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("✅ No obvious data quality issues found")

if __name__ == "__main__":
    analyze_csv_structure() 