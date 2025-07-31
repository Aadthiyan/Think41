import os
from pathlib import Path

def check_git_files():
    """Show which files should be pushed to GitHub"""
    
    print("=== Database Setup - Files to Push to GitHub ===")
    print("✅ These files SHOULD be pushed to GitHub:\n")
    
    # Files that should be pushed
    files_to_push = [
        "database_setup.py",
        "improved_database_setup.py", 
        "analyze_csv_structure.py",
        "query_database.py",
        "show_schema.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "check_git_files.py"
    ]
    
    for file in files_to_push:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (not found)")
    
    print("\n=== Files to IGNORE (not push to GitHub) ===")
    print("❌ These files should NOT be pushed to GitHub:\n")
    
    # Files that should NOT be pushed
    files_to_ignore = [
        "ecommerce.db",
        "ecommerce_improved.db", 
        "../archive/",
        "../__MACOSX/"
    ]
    
    for file in files_to_ignore:
        if os.path.exists(file):
            print(f"❌ {file} (will be ignored by .gitignore)")
        else:
            print(f"⚠️  {file} (not found)")
    
    print("\n=== Summary ===")
    print("📁 Total files in database_setup directory:", len([f for f in os.listdir('.') if os.path.isfile(f)]))
    print("✅ Files to push:", len([f for f in files_to_push if os.path.exists(f)]))
    print("❌ Files to ignore:", len([f for f in files_to_ignore if os.path.exists(f)]))
    
    print("\n=== Git Commands ===")
    print("To initialize and push to GitHub from database_setup folder:")
    print("1. git init")
    print("2. git add .")
    print("3. git commit -m 'Initial commit: E-commerce database setup'")
    print("4. git branch -M main")
    print("5. git remote add origin <your-github-repo-url>")
    print("6. git push -u origin main")
    
    print("\n=== Project Structure ===")
    print("📂 database_setup/")
    for file in sorted(os.listdir('.')):
        if os.path.isfile(file):
            print(f"   📄 {file}")

if __name__ == "__main__":
    check_git_files() 