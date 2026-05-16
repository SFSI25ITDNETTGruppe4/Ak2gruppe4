#!/usr/bin/env python3
"""
Script for å kjøre setup SQL på RDS database
"""
import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database config from .env
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "varehusdb")

print(f"Database config:")
print(f"  Host: {DB_HOST}")
print(f"  User: {DB_USER}")
print(f"  Database: {DB_NAME}")
print()

# Read SQL setup script
try:
    with open("db/setup_api_features.sql", "r") as f:
        sql_script = f.read()
except FileNotFoundError:
    print("ERROR: db/setup_api_features.sql not found")
    sys.exit(1)

# Connect to database
try:
    print("Connecting to database...")
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Connected!")
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    sys.exit(1)

# Execute SQL script
try:
    with connection.cursor() as cursor:
        # Split script into individual statements
        statements = [s.strip() for s in sql_script.split(';') if s.strip()]
        
        for i, statement in enumerate(statements, 1):
            print(f"\n[{i}/{len(statements)}] Executing...")
            print(f"  {statement[:80]}...")
            cursor.execute(statement)
            connection.commit()
            print(f"  ✅ Success")
    
    print("\n" + "="*50)
    print("✅ Setup complete!")
    print("="*50)

except Exception as e:
    print(f"\n❌ Error executing SQL: {str(e)}")
    sys.exit(1)

finally:
    connection.close()
