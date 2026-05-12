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
    cur.execute("DROP VIEW IF EXISTS olist.kpi_monthly_trend CASCADE")
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
    # NOTE: lead_behaviour_profile is only recorded in closed_deals (post-conversion).
    # This view shows profile distribution among closed deals, not MQL conversion prediction.
    # 100% conversion for profiled leads is expected — profiles are assigned at deal stage.
    print("\n5. Creating KPI: Lead Behavior...")
    cur.execute("""
        CREATE VIEW olist.kpi_lead_behavior AS
        SELECT 
            CASE 
                WHEN cd.lead_behaviour_profile = 'cat' THEN 'Cat'
                WHEN cd.lead_behaviour_profile = 'wolf' THEN 'Wolf'
                WHEN cd.lead_behaviour_profile = 'shark' THEN 'Shark'
                WHEN cd.lead_behaviour_profile = 'eagle' THEN 'Eagle'
                ELSE 'Unassigned'
            END AS lead_group,
            COUNT(DISTINCT cd.mql_id) AS closed_deals,
            ROUND(COUNT(DISTINCT cd.mql_id)::NUMERIC 
                / (SELECT COUNT(*) FROM olist.closed_deals) * 100, 2) AS pct_of_closed_deals,
            COUNT(DISTINCT cd.seller_id) AS sellers_with_orders
        FROM olist.closed_deals cd
        WHERE cd.lead_behaviour_profile IS NOT NULL
        GROUP BY 1
        ORDER BY 2 DESC
    """)
    conn.commit()
    print("   kpi_lead_behavior created")
    
    # KPI View 5: Time-to-Close Analysis
    print("\n6. Creating KPI: Time-to-Close...")
    cur.execute("""
        CREATE VIEW olist.kpi_time_to_close AS
        SELECT 
            DATE_TRUNC('month', mql.first_contact_date) AS month,
            AVG((cd.won_date::date - mql.first_contact_date::date)) AS avg_days_to_close,
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
    # Shows two things:
    # 1. Channel-level MQL-to-deal conversion (in 'Unassigned' rows)
    # 2. Lead behavior profile distribution within each channel's closed deals
    print("\n7. Creating KPI: Channel × Lead Behavior Cross-Tab...")
    cur.execute("""
        CREATE VIEW olist.kpi_channel_lead_behavior AS
        WITH channel_mqls AS (
            SELECT origin, COUNT(*) AS total_mqls
            FROM olist.marketing_qualified_leads
            GROUP BY 1
        ),
        channel_deals AS (
            SELECT mql.origin, COUNT(DISTINCT cd.mql_id) AS total_deals
            FROM olist.marketing_qualified_leads mql
            JOIN olist.closed_deals cd USING (mql_id)
            GROUP BY 1
        ),
        profile_deals AS (
            SELECT mql.origin,
                CASE 
                    WHEN cd.lead_behaviour_profile = 'cat' THEN 'Cat'
                    WHEN cd.lead_behaviour_profile = 'wolf' THEN 'Wolf'
                    WHEN cd.lead_behaviour_profile = 'shark' THEN 'Shark'
                    WHEN cd.lead_behaviour_profile = 'eagle' THEN 'Eagle'
                    ELSE 'Unassigned'
                END AS lead_group,
                COUNT(DISTINCT cd.mql_id) AS profile_deal_count
            FROM olist.marketing_qualified_leads mql
            JOIN olist.closed_deals cd USING (mql_id)
            GROUP BY 1, 2
        )
        SELECT 
            cm.origin,
            cm.total_mqls,
            cd.total_deals,
            ROUND(cd.total_deals::NUMERIC / cm.total_mqls * 100, 2) AS channel_conversion_pct,
            pd.lead_group,
            pd.profile_deal_count,
            ROUND(pd.profile_deal_count::NUMERIC / cd.total_deals * 100, 2) AS pct_of_channel_deals,
            ROUND(pd.profile_deal_count::NUMERIC / NULLIF(cm.total_mqls, 0) * 100, 2) AS mql_to_profile_deal_pct
        FROM channel_mqls cm
        LEFT JOIN channel_deals cd USING (origin)
        LEFT JOIN profile_deals pd USING (origin)
        ORDER BY cm.total_mqls DESC, pd.profile_deal_count DESC
    """)
    conn.commit()
    print("   kpi_channel_lead_behavior created")
    
    # KPI View 8 (NEW): Monthly Trend - Volume × Conversion × Time-to-Close
    print("\n8. Creating KPI: Monthly Trend...")
    cur.execute("""
        CREATE VIEW olist.kpi_monthly_trend AS
        WITH monthly_mqls AS (
            SELECT 
                DATE_TRUNC('month', first_contact_date)::DATE AS month,
                origin,
                COUNT(*) AS mql_count
            FROM olist.marketing_qualified_leads
            WHERE origin NOT IN ('NaN')
            GROUP BY 1, 2
        ),
        monthly_deals AS (
            SELECT 
                DATE_TRUNC('month', mql.first_contact_date)::DATE AS month,
                mql.origin,
                COUNT(DISTINCT cd.mql_id) AS deal_count
            FROM olist.marketing_qualified_leads mql
            JOIN olist.closed_deals cd USING (mql_id)
            WHERE mql.origin NOT IN ('NaN')
            GROUP BY 1, 2
        ),
        monthly_close AS (
            SELECT 
                DATE_TRUNC('month', mql.first_contact_date)::DATE AS month,
                AVG((cd.won_date::date - mql.first_contact_date::date)) AS avg_days_to_close,
                COUNT(DISTINCT cd.mql_id) AS deals_won
            FROM olist.marketing_qualified_leads mql
            JOIN olist.closed_deals cd USING (mql_id)
            WHERE cd.won_date IS NOT NULL AND mql.origin NOT IN ('NaN')
            GROUP BY 1
        )
        SELECT 
            mm.month,
            mm.origin,
            mm.mql_count,
            COALESCE(md.deal_count, 0) AS deal_count,
            COALESCE(ROUND(md.deal_count::NUMERIC / NULLIF(mm.mql_count, 0) * 100, 2), 0) AS conversion_pct,
            mc.avg_days_to_close,
            mc.deals_won
        FROM monthly_mqls mm
        LEFT JOIN monthly_deals md USING (month, origin)
        LEFT JOIN monthly_close mc USING (month)
        WHERE mm.origin IN ('organic_search', 'paid_search', 'social', 'direct_traffic', 'email', 'referral')
        ORDER BY mm.month, mm.mql_count DESC
    """)
    conn.commit()
    print("   kpi_monthly_trend created")
    
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
    print("\n3. Lead Behavior Profiles (distribution within closed deals):")
    cur.execute("""
        SELECT 
            lead_group,
            closed_deals,
            pct_of_closed_deals,
            sellers_with_orders
        FROM olist.kpi_lead_behavior
        ORDER BY 2 DESC
    """)
    for row in cur.fetchall():
        print(f"   {row[0]:10} | Deals: {row[1]:3} ({row[2]}%) | Sellers w/ orders: {row[3]}")
    
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
            total_mqls,
            total_deals,
            channel_conversion_pct,
            lead_group,
            profile_deal_count,
            pct_of_channel_deals
        FROM olist.kpi_channel_lead_behavior
        WHERE origin NOT IN ('NaN') AND origin IS NOT NULL
        ORDER BY total_mqls DESC, pct_of_channel_deals DESC
    """)
    for row in cur.fetchall():
        print(f"   {row[0]:18} | MQLs:{row[1]:5} | Deals:{row[2]:4} | Conv:{row[3]:6}% | {row[4]:10}:{row[5]:3} ({row[6]:6}% of channel)")
    
    # Monthly Trend
    print("\n6. Monthly Trend (MQL volume + conversion by channel):")
    cur.execute("""
        SELECT 
            month,
            origin,
            mql_count,
            conversion_pct,
            avg_days_to_close,
            deals_won
        FROM olist.kpi_monthly_trend
        ORDER BY month, mql_count DESC
    """)
    for row in cur.fetchall():
        ym = row[0].strftime('%Y-%m') if hasattr(row[0], 'strftime') else str(row[0])[:7]
        conv = float(row[3]) if row[3] is not None else 0.0
        close = f" | Close:{float(row[4]):.0f}d" if row[4] is not None else ""
        mql = int(row[2]) if row[2] is not None else 0
        print(f"   {ym} | {row[1]:18} | MQLs:{mql:4} | Conv:{conv:6.2f}%{close}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_funnel_kpis()
    verify_funnel_kpis()
    print("\n=== Phase 5 Complete ===")
