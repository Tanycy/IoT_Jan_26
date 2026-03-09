import sqlite3
import pandas as pd

DB = "perak_flights.db"
conn = sqlite3.connect(DB)
c = conn.cursor()

print("=" * 50)
print("CLEANING DATABASE")
print("=" * 50)

# ── 1. Trim trailing spaces on flight_number in flights ──
print("\n[1] Trimming flight_number spaces in flights table...")
c.execute("UPDATE flights SET flight_number = TRIM(flight_number)")
print(f"    Done. Rows affected: {c.rowcount}")

# ── 2. Remove rows with empty flight_number ──────────────
print("\n[2] Removing empty flight_number rows...")
c.execute("SELECT COUNT(*) FROM flights WHERE flight_number IS NULL OR flight_number = ''")
count = c.fetchone()[0]
c.execute("DELETE FROM flights WHERE flight_number IS NULL OR flight_number = ''")
print(f"    Removed {count} rows.")

# ── 3. Fix duplicate flight_numbers in flight_routes ─────
print("\n[3] Removing duplicate flight_numbers in flight_routes...")
print("    Keeping best record per flight (opensky > aerodatabox > hub_fallback > unknown)")

# Priority: opensky best, then aerodatabox, then hub_fallback, then null
c.execute("""
    DELETE FROM flight_routes
    WHERE id NOT IN (
        SELECT id FROM (
            SELECT id,
                   flight_number,
                   ROW_NUMBER() OVER (
                       PARTITION BY flight_number
                       ORDER BY
                           CASE source
                               WHEN 'opensky'      THEN 1
                               WHEN 'aerodatabox'  THEN 2
                               WHEN 'hub_fallback' THEN 3
                               ELSE 4
                           END
                   ) AS rn
            FROM flight_routes
        ) ranked
        WHERE rn = 1
    )
""")
print(f"    Removed {c.rowcount} duplicate rows.")

# ── 4. Fill null source ───────────────────────────────────
print("\n[4] Filling null source values...")
c.execute("UPDATE flight_routes SET source = 'unknown' WHERE source IS NULL")
print(f"    Updated {c.rowcount} rows.")

# ── 5. Trim flight_number in flight_routes too ────────────
print("\n[5] Trimming flight_number spaces in flight_routes...")
c.execute("UPDATE flight_routes SET flight_number = TRIM(flight_number)")
print(f"    Done.")

conn.commit()

# ── Final summary ─────────────────────────────────────────
print("\n" + "=" * 50)
print("FINAL SUMMARY")
print("=" * 50)

c.execute("SELECT COUNT(*) FROM flights")
print(f"flights rows        : {c.fetchone()[0]}")

c.execute("SELECT COUNT(*) FROM flight_routes")
print(f"flight_routes rows  : {c.fetchone()[0]}")

c.execute("SELECT COUNT(DISTINCT flight_number) FROM flight_routes")
print(f"unique routes saved : {c.fetchone()[0]}")

c.execute("SELECT source, COUNT(*) FROM flight_routes GROUP BY source")
print("\nRoutes by source:")
for row in c.fetchall():
    print(f"  {row[0]:15} : {row[1]}")

# Check join coverage
c.execute("""
    SELECT COUNT(DISTINCT f.flight_number) 
    FROM flights f
    INNER JOIN flight_routes r ON f.flight_number = r.flight_number
""")
matched = c.fetchone()[0]
c.execute("SELECT COUNT(DISTINCT flight_number) FROM flights")
total = c.fetchone()[0]
print(f"\nDashboard coverage  : {matched}/{total} unique flights have departure airport")

conn.close()
print("\nCleaning complete!")
