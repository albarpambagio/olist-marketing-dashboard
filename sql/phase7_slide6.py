import psycopg2

DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'olist'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

def create_slide6_view():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    print("=" * 50)
    print("PHASE 7: SLIDE 6 — PROFILE BY CHANNEL")
    print("=" * 50)

    print("\n1. Cleaning up existing view...")
    cur.execute("DROP VIEW IF EXISTS olist.vw_profile_by_channel CASCADE")
    conn.commit()
    print("   Done")

    print("\n2. Creating vw_profile_by_channel...")
    cur.execute("""
        CREATE VIEW olist.vw_profile_by_channel AS
        SELECT 
            mql.origin,
            CASE 
                WHEN cd.lead_behaviour_profile = 'cat' THEN 'Cat'
                WHEN cd.lead_behaviour_profile = 'wolf' THEN 'Wolf'
                WHEN cd.lead_behaviour_profile = 'shark' THEN 'Shark'
                WHEN cd.lead_behaviour_profile = 'eagle' THEN 'Eagle'
                ELSE 'Unassigned'
            END AS lead_group,
            COUNT(DISTINCT cd.mql_id) AS deal_count
        FROM olist.marketing_qualified_leads mql
        JOIN olist.closed_deals cd USING (mql_id)
        GROUP BY 1, 2
        ORDER BY 1, 2
    """)
    conn.commit()
    print("   vw_profile_by_channel created")

    print("\n3. Verification...")
    cur.execute("SELECT origin, lead_group, deal_count FROM olist.vw_profile_by_channel ORDER BY origin, lead_group")
    rows = cur.fetchall()
    print(f"   Rows: {len(rows)}")
    for r in rows:
        print(f"     {r[0]:25s} {r[1]:15s} {r[2]}")

    cur.close()
    conn.close()
    print("\n=== Phase 7 Complete ===")

if __name__ == '__main__':
    create_slide6_view()
