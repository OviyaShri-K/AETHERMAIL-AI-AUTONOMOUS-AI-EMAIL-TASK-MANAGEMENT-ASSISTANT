import os
import subprocess
import time

def reset_password():
    hba_path = r"C:\Program Files\PostgreSQL\18\data\pg_hba.conf"
    
    print("1. Backing up and updating pg_hba.conf to trust mode...")
    with open(hba_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace scram-sha-256 with trust
    trust_content = content.replace("scram-sha-256", "trust")
    with open(hba_path, "w", encoding="utf-8") as f:
        f.write(trust_content)
        
    print("2. Restarting PostgreSQL Windows service...")
    subprocess.run(["powershell", "-Command", "Restart-Service -Name postgresql-x64-18"], check=True)
    time.sleep(2)
    
    psql_path = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
    
    print("3. Setting password for user 'postgres' to 'admin'...")
    subprocess.run([psql_path, "-U", "postgres", "-h", "127.0.0.1", "-c", "ALTER USER postgres WITH PASSWORD 'admin';"], check=True)
    
    print("4. Creating database 'ai_email_db' if not exists...")
    subprocess.run([psql_path, "-U", "postgres", "-h", "127.0.0.1", "-c", "CREATE DATABASE ai_email_db;"])
    
    print("5. Restoring pg_hba.conf to secure mode...")
    with open(hba_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    subprocess.run(["powershell", "-Command", "Restart-Service -Name postgresql-x64-18"], check=True)
    
    print("\n" + "="*70)
    print(" ✅ SUCCESS! POSTGRESQL PASSWORD IS NOW: 'admin'")
    print(" ✅ LOCAL DATABASE: 'ai_email_db' (or 'postgres')")
    print(" ✅ CONNECTION STRING: postgresql://postgres:admin@localhost:5432/ai_email_db")
    print("="*70 + "\n")

if __name__ == "__main__":
    reset_password()
