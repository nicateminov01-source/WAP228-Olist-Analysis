import os
import sqlite3
import pandas as pd

DB_NAME = "olist_ecommerce.db"
DATA_DIR = "data"
SCHEMA_FILE = "schema.sql"

def init_db():
    """Initializes the database according to the schema."""
    print("[+] Creating database schema...")
    with sqlite3.connect(DB_NAME) as conn:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    print("[+] Schema applied successfully.")

def load_csv_to_sql():
    """Reads CSV files and transfers them to SQL tables."""
    # CSV Filenames -> SQL Table Names Mapping
    files_to_tables = {
        "olist_customers_dataset.csv": "customers",
        "olist_products_dataset.csv": "products",
        "product_category_name_translation.csv": "category_translation",
        "olist_orders_dataset.csv": "orders",
        "olist_order_items_dataset.csv": "order_items",
        "olist_order_payments_dataset.csv": "order_payments"
    }

    conn = sqlite3.connect(DB_NAME)
    
    for csv_file, table_name in files_to_tables.items():
        file_path = os.path.join(DATA_DIR, csv_file)
        
        if not os.path.exists(file_path):
            print(f"[!] Error: {file_path} not found! Please add the data to the 'data' folder.")
            continue
            
        print(f"[->] Reading {csv_file} and transferring to the '{table_name}' table...")
        
        df = pd.read_csv(file_path)
        
        # Append data to the existing schema
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"[+] '{table_name}' table successfully populated. Row count: {len(df)}")

    conn.close()
    print("[+] All data transfer processes completed successfully!")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    init_db()
    load_csv_to_sql()
