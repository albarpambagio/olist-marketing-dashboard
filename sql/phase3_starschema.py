import psycopg2

DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'olist'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

def create_marketing_schema():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    print("=" * 50)
    print("PHASE 3: MARKETING STAR SCHEMA")
    print("=" * 50)
    
    # Drop existing views
    print("\n1. Cleaning up existing views...")
    cur.execute("DROP VIEW IF EXISTS olist.fact_marketing CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.dim_marketing CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.dim_channel CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.dim_seller CASCADE")
    conn.commit()
    print("   Done")
    
    # Create dim_date (reuse from e-commerce)
    print("\n2. Creating dim_date (reuse)...")
    cur.execute("""
        CREATE OR REPLACE VIEW olist.dim_date AS
        SELECT
            d::DATE                                AS date_key,
            EXTRACT(YEAR FROM d)::INT              AS year,
            EXTRACT(QUARTER FROM d)::INT           AS quarter,
            TO_CHAR(d, 'YYYY-MM')                  AS year_month,
            EXTRACT(MONTH FROM d)::INT             AS month,
            TO_CHAR(d, 'Month')                    AS month_name,
            EXTRACT(WEEK FROM d)::INT             AS week_num,
            EXTRACT(DOW FROM d)::INT              AS day_of_week,
            CASE WHEN EXTRACT(DOW FROM d) IN (0,6)
                 THEN TRUE ELSE FALSE END          AS is_weekend
        FROM GENERATE_SERIES('2016-01-01'::DATE, '2019-12-31'::DATE, '1 day') d;
    """)
    conn.commit()
    print("   dim_date created")
    
    # Create dim_channel (from marketing data)
    print("\n3. Creating dim_channel...")
    cur.execute("""
        CREATE OR REPLACE VIEW olist.dim_channel AS
        SELECT DISTINCT
            origin AS channel_id,
            origin AS channel_name
        FROM olist.marketing_qualified_leads
        ORDER BY 2;
    """)
    conn.commit()
    print("   dim_channel created")
    
    # Create dim_marketing (marketing qualified leads + closed deals)
    print("\n4. Creating dim_marketing...")
    cur.execute("""
        CREATE OR REPLACE VIEW olist.dim_marketing AS
        SELECT
            mql.mql_id,
            mql.first_contact_date,
            mql.origin,
            mql.landing_page_id,
            cd.lead_behaviour_profile,
            cd.business_segment,
            cd.lead_type,
            cd.seller_id,
            cd.won_date,
            cd.has_company,
            cd.has_gtin,
            cd.average_stock,
            cd.business_type,
            cd.declared_product_catalog_size,
            cd.declared_monthly_revenue
        FROM olist.marketing_qualified_leads mql
        LEFT JOIN olist.closed_deals cd USING (mql_id)
        ORDER BY mql.first_contact_date;
    """)
    conn.commit()
    print("   dim_marketing created")
    
    # Create fact_marketing (combined with e-commerce revenue)
    print("\n5. Creating fact_marketing (combined schema)...")
    cur.execute("""
        CREATE OR REPLACE VIEW olist.fact_marketing AS
        SELECT
            dm.mql_id,
            dm.seller_id,
            dm.first_contact_date::DATE          AS lead_date,
            dm.won_date::DATE                  AS won_date,
            dm.origin,
            dm.lead_behaviour_profile,
            dm.business_segment,
            fo.order_date,
            fo.revenue,
            fo.freight_value,
            fo.review_score,
            fo.is_late,
            fo.is_repeat_customer,
            (dm.won_date::date - dm.first_contact_date::date) AS days_to_close
        FROM olist.dim_marketing dm
        LEFT JOIN olist.fact_orders fo ON dm.seller_id = fo.seller_id
        ORDER BY dm.first_contact_date;
    """)
    conn.commit()
    print("   fact_marketing created")
    
    # Create dim_seller (bridge between fact_marketing and fact_orders)
    print("\n6. Creating dim_seller...")
    cur.execute("""
        CREATE OR REPLACE VIEW olist.dim_seller AS
        SELECT DISTINCT
            seller_id,
            seller_zip_code_prefix,
            seller_city,
            seller_state
        FROM olist.sellers
        ORDER BY seller_id;
    """)
    conn.commit()
    print("   dim_seller created")
    
    # Verify
    print("\n=== Verification ===")
    cur.execute("SELECT COUNT(*) FROM olist.dim_marketing;")
    print(f"   dim_marketing: {cur.fetchone()[0]:,} rows")
    cur.execute("SELECT COUNT(*) FROM olist.fact_marketing;")
    print(f"   fact_marketing: {cur.fetchone()[0]:,} rows")
    cur.execute("SELECT COUNT(*) FROM olist.dim_seller;")
    print(f"   dim_seller: {cur.fetchone()[0]:,} rows")
    cur.execute("SELECT COUNT(DISTINCT origin) FROM olist.dim_marketing;")
    print(f"   Channels: {cur.fetchone()[0]}")
    
    cur.close()
    conn.close()
    print("\n=== Phase 3 Complete ===")

if __name__ == '__main__':
    create_marketing_schema()
