#!/usr/bin/env python
"""
MariaDB Setup Helper for News Application
"""

import subprocess
import sys
import os

def run_command(command):
    """Execute a shell command"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 MariaDB Setup for News Application")
    print("=" * 50)
    
    # Check if MySQL client is available
    success, stdout, stderr = run_command("which mysql")
    if not success:
        print(" MySQL client not found.")
        print("   Please install MariaDB first:")
        print("   On macOS: brew install mariadb")
        print("   On Ubuntu: sudo apt-get install mariadb-server")
        return
    
    print("MySQL client found")
    
    # Instructions for MariaDB setup
    print("\nManual Setup Steps Required:")
    print("1. Start MariaDB service:")
    print("   brew services start mariadb  # macOS")
    print("   sudo systemctl start mariadb  # Linux")
    
    print("\n2. Create database and user:")
    print("   mysql -u root -p")
    print("   CREATE DATABASE news_app_db;")
    print("   CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'news_password';")
    print("   GRANT ALL PRIVILEGES ON news_app_db.* TO 'news_user'@'localhost';")
    print("   FLUSH PRIVILEGES;")
    print("   EXIT;")
    
    print("\n3. Update Django settings:")
    print("   Edit news_project/settings.py:")
    print("   - Uncomment the MariaDB DATABASES configuration")
    print("   - Update NAME, USER, PASSWORD with your values")
    
    print("\n4. Run migrations:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
    print("\n5. Create superuser:")
    print("   python manage.py createsuperuser")
    
    print("\n6. Test the application:")
    print("   python manage.py runserver")
    print("   python manage.py test  # Run tests against MariaDB")
    
    print("\nOptional: Migrate existing data")
    print("   If you want to keep current SQLite data:")
    print("   python manage.py dumpdata --indent=2 > backup.json")
    print("   # After switching to MariaDB:")
    print("   python manage.py loaddata backup.json")
    
    print("\n" + "=" * 50)
    print("Setup instructions complete!")
    print("   Follow the steps above to migrate to MariaDB.")

if __name__ == "__main__":
    main()
