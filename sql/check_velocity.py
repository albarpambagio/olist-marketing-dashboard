import psycopg2

conn = psycopg2.connect(host='localhost', port='5433', dbname='olist', user='postgres', password='admin')
cur = conn.cursor()

print("=== Time-to-Close by Month (All Data) ===\n")
print("Month       | Avg Days to Close | Deals Won")
print("-" * 50)

cur.execute("""
    SELECT 
        TO_CHAR(month, 'YYYY-MM') AS month,
        ROUND(avg_days_to_close, 1) AS avg_days,
        deals_won
    FROM olist.kpi_time_to_close
    ORDER BY month
""")

for row in cur.fetchall():
    print(f"{row[0]}     | {row[1]:17} | {row[2]}")

print("\n=== Filtered: Jan 2018 - May 2018 ===\n")
print("Month       | Avg Days to Close | Deals Won")
print("-" * 50)

cur.execute("""
    SELECT 
        TO_CHAR(month, 'YYYY-MM') AS month,
        ROUND(avg_days_to_close, 1) AS avg_days,
        deals_won
    FROM olist.kpi_time_to_close
    WHERE month >= '2018-01-01' AND month <= '2018-05-31'
    ORDER BY month
""")

for row in cur.fetchall():
    print(f"{row[0]}     | {row[1]:17} | {row[2]}")

conn.close()