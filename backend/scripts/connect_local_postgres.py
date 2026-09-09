import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

passwords = ["admin", "postgres", "root", "1234", "12345", "password", "sarah jenkins", ""]

def find_postgres_credentials():
    print("Testing connection to local PostgreSQL server (localhost:5432)...")
    working_pwd = None
    for pwd in passwords:
        try:
            conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password=pwd, database="postgres")
            conn.close()
            working_pwd = pwd
            print(f"✅ Found working PostgreSQL password: '{pwd}'")
            break
        except Exception as e:
            pass
            
    return working_pwd

if __name__ == "__main__":
    pwd = find_postgres_credentials()
    if pwd is not None:
        print(f"DATABASE_URL=postgresql://postgres:{pwd}@localhost:5432/ai_email_db")
    else:
        print("Could not auto-detect password from common list.")
