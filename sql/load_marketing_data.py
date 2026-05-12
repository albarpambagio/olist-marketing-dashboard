import psycopg2
import pandas as pd
import os
from psycopg2.extras import execute_values

DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'olist'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

def load_marketing_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    print("=" * 50)
    print("LOADING MARKETING FUNNEL DATA")
    print("=" * 50)
    
    cur.execute("CREATE SCHEMA IF NOT EXISTS olist;")
    conn.commit()
    
    # Load olist_marketing_qualified_leads_dataset.csv
    # CSV has 4 columns: mql_id, first_contact_date, landing_page_id, origin
    print("\n1. Loading Marketing Qualified Leads...")
    mql_file = 'data/olist_marketing_qualified_leads_dataset.csv'
    if os.path.exists(mql_file):
        df = pd.read_csv(mql_file)
        print(f"   Found {len(df)} rows in {mql_file}")
        
        cur.execute("""
            DROP TABLE IF EXISTS olist.marketing_qualified_leads CASCADE;
            CREATE TABLE olist.marketing_qualified_leads (
                mql_id VARCHAR(50),
                first_contact_date DATE,
                landing_page_id VARCHAR(50),
                origin VARCHAR(50)
            );
        """)
        conn.commit()
        
        rows = [(r['mql_id'], r['first_contact_date'], r['landing_page_id'], r['origin'])
                for _, r in df.iterrows()]
        execute_values(cur,
            "INSERT INTO olist.marketing_qualified_leads VALUES %s",
            rows)
        conn.commit()
        print(f"   Loaded {len(df)} rows into olist.marketing_qualified_leads")
    else:
        print(f"   File not found: {mql_file}")
    
    # Load olist_closed_deals_dataset.csv
    print("\n2. Loading Closed Deals...")
    deals_file = 'data/olist_closed_deals_dataset.csv'
    if os.path.exists(deals_file):
        df = pd.read_csv(deals_file)
        print(f"   Found {len(df)} rows in {deals_file}")
        
        # Create table
        cur.execute("""
            DROP TABLE IF EXISTS olist.closed_deals CASCADE;
            CREATE TABLE olist.closed_deals (
                mql_id VARCHAR(50),
                seller_id VARCHAR(50),
                sdr_id VARCHAR(50),
                sr_id VARCHAR(50),
                won_date DATE,
                business_segment VARCHAR(100),
                lead_type VARCHAR(50),
                lead_behaviour_profile VARCHAR(50),
                has_company BOOLEAN,
                has_gtin BOOLEAN,
                average_stock VARCHAR(20),
                business_type VARCHAR(50),
                declared_product_catalog_size VARCHAR(20),
                declared_monthly_revenue VARCHAR(20)
            );
        """)
        conn.commit()
        
        # Insert data (convert NaN to None for psycopg2 compatibility)
        df = df.where(df.notna(), None)

        def safe_bool(val):
            return None if val is None else bool(val)

        rows = [(r['mql_id'], r['seller_id'], r['sdr_id'], r['sr_id'],
                 r['won_date'], r['business_segment'], r['lead_type'],
                 r['lead_behaviour_profile'], safe_bool(r['has_company']), safe_bool(r['has_gtin']),
                 str(r['average_stock']) if r['average_stock'] is not None else None,
                 r['business_type'],
                 str(r['declared_product_catalog_size']) if r['declared_product_catalog_size'] is not None else None,
                 str(r['declared_monthly_revenue']) if r['declared_monthly_revenue'] is not None else None)
                for _, r in df.iterrows()]
        execute_values(cur,
            "INSERT INTO olist.closed_deals VALUES %s",
            rows)
        conn.commit()
        print(f"   Loaded {len(df)} rows into olist.closed_deals")
    else:
        print(f"   File not found: {deals_file}")
    
    # Verify row counts
    print("\n3. Verification:")
    cur.execute("SELECT COUNT(*) FROM olist.marketing_qualified_leads;")
    print(f"   MQLs: {cur.fetchone()[0]:,}")
    cur.execute("SELECT COUNT(*) FROM olist.closed_deals;")
    print(f"   Closed Deals: {cur.fetchone()[0]:,}")
    
    cur.close()
    conn.close()
    print("\n=== Marketing Data Load Complete ===")

if __name__ == '__main__':
    load_marketing_data()
