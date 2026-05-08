import psycopg2
import pandas as pd
import os

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
    
    # Create schema if not exists
    cur.execute("CREATE SCHEMA IF NOT EXISTS olist;")
    conn.commit()
    
    # Load olist_marketing_qualified_leads_dataset.csv
    print("\n1. Loading Marketing Qualified Leads...")
    mql_file = 'data/olist_marketing_qualified_leads_dataset.csv'
    if os.path.exists(mql_file):
        df = pd.read_csv(mql_file)
        print(f"   Found {len(df)} rows in {mql_file}")
        
        # Create table
        cur.execute("""
            DROP TABLE IF EXISTS olist.marketing_qualified_leads CASCADE;
            CREATE TABLE olist.marketing_qualified_leads (
                mql_id VARCHAR(50),
                first_contact_date DATE,
                landing_page_id VARCHAR(50),
                origin VARCHAR(50),
                seller_id VARCHAR(50),
                sdr_id VARCHAR(50),
                sr_id VARCHAR(50),
                won_date DATE,
                business_segment VARCHAR(100),
                lead_type VARCHAR(50),
                lead_behaviour_profile VARCHAR(50),
                has_company BOOLEAN,
                has_gtin BOOLEAN,
                average_stock INTEGER,
                business_type VARCHAR(50),
                declared_product_catalog_size INTEGER,
                declared_monthly_revenue NUMERIC
            );
        """)
        conn.commit()
        
        # Insert data
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO olist.marketing_qualified_leads VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                row.get('mql_id'),
                row.get('first_contact_date'),
                row.get('landing_page_id'),
                row.get('origin'),
                row.get('seller_id'),
                row.get('sdr_id'),
                row.get('sr_id'),
                row.get('won_date'),
                row.get('business_segment'),
                row.get('lead_type'),
                row.get('lead_behaviour_profile'),
                row.get('has_company'),
                row.get('has_gtin'),
                row.get('average_stock'),
                row.get('business_type'),
                row.get('declared_product_catalog_size'),
                row.get('declared_monthly_revenue')
            ))
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
                won_date DATE,
                business_segment VARCHAR(100),
                lead_type VARCHAR(50),
                lead_behaviour_profile VARCHAR(50),
                has_company BOOLEAN,
                has_gtin BOOLEAN,
                average_stock INTEGER,
                business_type VARCHAR(50),
                declared_product_catalog_size INTEGER,
                declared_monthly_revenue NUMERIC
            );
        """)
        conn.commit()
        
        # Insert data
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO olist.closed_deals VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                row.get('mql_id'),
                row.get('seller_id'),
                row.get('won_date'),
                row.get('business_segment'),
                row.get('lead_type'),
                row.get('lead_behaviour_profile'),
                row.get('has_company'),
                row.get('has_gtin'),
                row.get('average_stock'),
                row.get('business_type'),
                row.get('declared_product_catalog_size'),
                row.get('declared_monthly_revenue')
            ))
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
