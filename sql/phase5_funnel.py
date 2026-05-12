import psycopg2

DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'olist'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

def create_funnel_kpis():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    print("=" * 50)
    print("PHASE 5: MARKETING FUNNEL KPIs")
    print("=" * 50)
    
    # Drop existing views
    print("\n1. Cleaning up existing funnel views...")
    cur.execute("DROP VIEW IF EXISTS olist.kpi_mql_volume CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.kpi_conversion_rate CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.kpi_ltv_by_channel CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.kpi_lead_behavior CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.kpi_channel_lead_behavior CASCADE")
    cur.execute("DROP VIEW IF EXISTS olist.kpi_time_to_close CASCADE")
    conn.commit()
    print("   Done")
    
    # KPI View 1: MQL Volume by Month + Channel
    print("\n2. Creating KPI: MQL Volume...")
    cur.execute("""
        CREATE VIEW olist.kpi_mql_volume AS
        SELECT 
            DATE_TRUNC('month', first_contact_date) AS month,
            origin,
            COUNT(*) AS mql_count
        FROM olist.marketing_qualified_leads
        GROUP BY 1, 2
        ORDER BY 1, 3 DESC
    """)
    conn.commit()
    print("   kpi_mql_volume created")
    
    # KPI View 2: Conversion Rate by Channel
    print("\n3. Creating KPI: Conversion Rate...")
    cur.execute("""
        CREATE VIEW olist.kpi_conversion_rate AS
        SELECT 
            mql.origin,
            COUNT(DISTINCT mql.mql_id) AS total_mqls,
            COUNT(DISTINCT cd.mql_id) AS closed_deals,
            ROUND(COUNT(DISTINCT cd.mql_id)::NUMERIC / COUNT(DISTINCT mql.mql_id) * 100, 2) AS conversion_rate_pct
        FROM olist.marketing_qualified_leads mql
        LEFT JOIN olist.closed_deals cd USING (mql_id)
        GROUP BY 1
        ORDER BY 3 DESC
    """)
    conn.commit()
    print("   kpi_conversion_rate created")
    
    # KPI View 3: LTV by Channel (Lifetime Value)
    # NOTE: Uses LEFT JOIN so COUNT(DISTINCT mql.mql_id) includes ALL MQLs,
    # not just converted ones. ltv_per_mql = revenue / total MQLs (conservative).
    # ltv_per_seller = revenue / sellers with orders (only converted + active).
    print("\n4. Creating KPI: LTV by Channel...")
    cur.execute("""
        CREATE VIEW olist.kpi_ltv_by_channel AS
        SELECT 
            mql.origin,
            COUNT(DISTINCT mql.mql_id) AS total_mqls,
            COUNT(DISTINCT cd.seller_id) AS sellers_acquired,
            COALESCE(SUM(fo.revenue), 0) AS total_revenue,
            ROUND(COALESCE(SUM(fo.revenue), 0)::NUMERIC 
                / NULLIF(COUNT(DISTINCT mql.mql_id), 0), 2) AS ltv_per_mql,
            ROUND(COALESCE(SUM(fo.revenue), 0)::NUMERIC 
                / NULLIF(COUNT(DISTINCT cd.seller_id), 0), 2) AS ltv_per_seller,
            COUNT(DISTINCT cd.mql_id) AS converted_mqls,
            ROUND(COUNT(DISTINCT cd.mql_id)::NUMERIC 
                / NULLIF(COUNT(DISTINCT mql.mql_id), 0) * 100, 2) AS conversion_rate_pct
        FROM olist.marketing_qualified_leads mql
        LEFT JOIN olist.closed_deals cd USING (mql_id)
        LEFT JOIN olist.sellers s ON cd.seller_id = s.seller_id
        LEFT JOIN olist.fact_orders fo ON s.seller_id = fo.seller_id
        GROUP BY 1
        ORDER BY 4 DESC
    """)
    conn.commit()
    print("   kpi_ltv_by_channel created")
    
    # KPI View 4: Lead Behavior Analysis
    print("\n5. Creating KPI: Lead Behavior...")
    cur.execute("""
        CREATE VIEW olist.kpi_lead_behavior AS
        SELECT 
            CASE 
                WHEN cd.lead_behaviour_profile = 'cat' THEN 'Cat'
                WHEN cd.lead_behaviour_profile = 'wolf' THEN 'Wolf'
                WHEN cd.lead_behaviour_profile = 'shark' THEN 'Shark'
                WHEN cd.lead_behaviour_profile = 'eagle' THEN 'Eagle'
                ELSE 'Other'
            END AS lead_group,
            COUNT(DISTINCT cd.mql_id) AS total_leads,
            COUNT(DISTINCT cd.seller_id) AS closed_deals,
            ROUND(COUNT(DISTINCT cd.seller_id)::NUMERIC / COUNT(DISTINCT cd.mql_id) * 100, 2) AS conversion_rate_pct
        FROM olist.closed_deals cd
        JOIN olist.marketing_qualified_leads mql USING (mql_id)
        GROUP BY 1
        ORDER BY 3 DESC
    """)
    conn.commit()
    print("   kpi_lead_behavior created")
    
    # KPI View 5: Time-to-Close Analysis
    print("\n6. Creating KPI: Time-to-Close...")
    cur.execute("""
        CREATE VIEW olist.kpi_time_to_close AS
        SELECT 
            DATE_TRUNC('month', mql.first_contact_date) AS month,
            AVG(DATE_PART('day', cd.won_date - mql.first_contact_date)) AS avg_days_to_close,
            COUNT(DISTINCT cd.seller_id) AS deals_won
        FROM olist.marketing_qualified_leads mql
        JOIN olist.closed_deals cd USING (mql_id)
        WHERE cd.won_date IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """)
    conn.commit()
    print("   kpi_time_to_close created")
    
    # KPI View 7 (NEW): Channel × Lead Behavior Cross-Tab
    print("\n7. Creating KPI: Channel × Lead Behavior Cross-Tab...")
    cur.execute("""
        CREATE VIEW olist.kpi_channel_lead_behavior AS
        SELECT 
            mql.origin,
            CASE 
                WHEN cd.lead_behaviour_profile = 'cat' THEN 'Cat'
                WHEN cd.lead_behaviour_profile = 'wolf' THEN 'Wolf'
                WHEN cd.lead_behaviour_profile = 'shark' THEN 'Shark'
                WHEN cd.lead_behaviour_profile = 'eagle' THEN 'Eagle'
                ELSE 'Other'
            END AS lead_group,
            COUNT(DISTINCT mql.mql_id) AS total_mqls,
            COUNT(DISTINCT cd.mql_id) AS closed_deals,
            ROUND(COUNT(DISTINCT cd.mql_id)::NUMERIC 
                / NULLIF(COUNT(DISTINCT mql.mql_id), 0) * 100, 2) AS conversion_rate_pct
        FROM olist.marketing_qualified_leads mql
        LEFT JOIN olist.closed_deals cd USING (mql_id)
        GROUP BY 1, 2
        ORDER BY 1, 5 DESC
    """)
    conn.commit()
    print("   kpi_channel_lead_behavior created")
    
    cur.close()
    conn.close()

def verify_funnel_kpis():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    print("\n=== Funnel KPI Verification ===")
    
    # Channel Performance
    print("\n1. Channel Performance (Conversion Rate):")
    cur.execute("""
        SELECT 
            origin,
            total_mqls,
            closed_deals,
            conversion_rate_pct
        FROM olist.kpi_conversion_rate
        ORDER BY 3 DESC
    """)
    for row in cur.fetchall():
        print(f"   {row[0]:15} | MQLs: {row[1]:4} | Deals: {row[2]:3} | Conv: {row[3]}%")
    
    # LTV by Channel
    print("\n2. LTV by Channel:")
    cur.execute("""
        SELECT 
            origin,
            total_mqls,
            sellers_acquired,
            total_revenue,
            ltv_per_mql,
            ltv_per_seller,
            conversion_rate_pct
        FROM olist.kpi_ltv_by_channel
        ORDER BY 4 DESC
    """)
    for row in cur.fetchall():
        print(f"   {row[0]:15} | MQLs: {row[1]:4} | Sellers: {row[2]:3} | Rev: ${row[3]:,.0f} | LTV/MQL: ${row[4]} | LTV/Seller: ${row[5]} | Conv: {row[6]}%")
    
    # Lead Behavior
    print("\n3. Lead Behavior Profiles:")
    cur.execute("""
        SELECT 
            lead_group,
            total_leads,
            closed_deals,
            conversion_rate_pct
        FROM olist.kpi_lead_behavior
        ORDER BY 4 DESC
    """)
    for row in cur.fetchall():
        print(f"   {row[0]:6} | Leads: {row[1]:4} | Deals: {row[2]:3} | Conv: {row[3]}%")
    
    # Time-to-Close Trend
    print("\n4. Time-to-Close Trend (last 6 months):")
    cur.execute("""
        SELECT 
            TO_CHAR(month, 'YYYY-MM') AS ym,
            ROUND(avg_days_to_close, 1) AS avg_days,
            deals_won
        FROM olist.kpi_time_to_close
        ORDER BY month DESC
        LIMIT 6
    """)
    for row in cur.fetchall():
        print(f"   {row[0]}: {row[1]} days avg, {row[2]} deals won")
    
    # Channel x Lead Behavior Cross-Tab
    print("\n5. Channel x Lead Behavior Cross-Tab:")
    cur.execute("""
        SELECT 
            origin,
            lead_group,
            total_mqls,
            closed_deals,
            conversion_rate_pct
        FROM olist.kpi_channel_lead_behavior
        WHERE origin IS NOT NULL
        ORDER BY 1, 5 DESC
    """)
    for row in cur.fetchall():
        print(f"   {row[0]:15} | {row[1]:6} | MQLs: {row[2]:4} | Deals: {row[3]:3} | Conv: {row[4]}%")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_funnel_kpis()
    verify_funnel_kpis()
    print("\n=== Phase 5 Complete ===")
