import psycopg2

conn = psycopg2.connect(host='localhost', port='5433', dbname='olist', user='postgres', password='admin')
cur = conn.cursor()

print("=== Comparing days_to_close calculation ===\n")

# Check 1: Rows in fact_marketing with non-null days_to_close
print("1. fact_marketing days_to_close breakdown:")
cur.execute("""
    SELECT
        COUNT(*) as total_rows,
        COUNT(days_to_close) as rows_with_days_to_close,
        COUNT(*) - COUNT(days_to_close) as rows_with_null
    FROM olist.fact_marketing
""")
row = cur.fetchone()
print(f"   Total rows: {row[0]}, With days_to_close: {row[1]}, NULL: {row[2]}")

# Check 2: Average by month from fact_marketing (DAX perspective)
print("\n2. fact_marketing - Monthly Avg Days to Close (Jan-May 2018):")
cur.execute("""
    SELECT
        TO_CHAR(lead_date, 'YYYY-MM') AS month,
        ROUND(AVG(days_to_close), 1) AS avg_days,
        COUNT(*) AS row_count
    FROM olist.fact_marketing
    WHERE lead_date >= '2018-01-01' AND lead_date <= '2018-05-31'
        AND days_to_close IS NOT NULL
    GROUP BY 1
    ORDER BY 1
""")
print("   Month    | Avg Days | Row Count")
print("   " + "-" * 35)
for row in cur.fetchall():
    print(f"   {row[0]}   | {row[1]:8} | {row[2]}")

# Check 3: From kpi_time_to_close view (SQL perspective)
print("\n3. kpi_time_to_close view - Monthly Avg Days to Close (Jan-May 2018):")
cur.execute("""
    SELECT
        TO_CHAR(month, 'YYYY-MM') AS month,
        ROUND(avg_days_to_close, 1) AS avg_days,
        deals_won
    FROM olist.kpi_time_to_close
    WHERE month >= '2018-01-01' AND month <= '2018-05-31'
    ORDER BY 1
""")
print("   Month    | Avg Days | Deals Won")
print("   " + "-" * 35)
for row in cur.fetchall():
    print(f"   {row[0]}   | {row[1]:8} | {row[2]}")

# Check 4: What if we filter by origin in fact_marketing?
print("\n4. fact_marketing - With origin filter (exclude 'unknown'):")
cur.execute("""
    SELECT
        TO_CHAR(lead_date, 'YYYY-MM') AS month,
        ROUND(AVG(days_to_close), 1) AS avg_days,
        COUNT(*) AS row_count
    FROM olist.fact_marketing
    WHERE lead_date >= '2018-01-01' AND lead_date <= '2018-05-31'
        AND days_to_close IS NOT NULL
        AND origin IS NOT NULL
        AND origin <> 'unknown'
        AND origin <> 'NaN'
    GROUP BY 1
    ORDER BY 1
""")
print("   Month    | Avg Days | Row Count")
print("   " + "-" * 35)
for row in cur.fetchall():
    print(f"   {row[0]}   | {row[1]:8} | {row[2]}")

conn.close()