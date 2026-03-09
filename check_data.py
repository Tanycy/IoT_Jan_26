import sqlite3
import pandas as pd

conn = sqlite3.connect("perak_flights.db")

print("=== flights table ===")
df = pd.read_sql_query("SELECT * FROM flights", conn)
print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nNull counts:")
print(df.isnull().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"\nFlight number empty/null: {df['flight_number'].isna().sum() + (df['flight_number'].str.strip() == '').sum()}")
print(f"\nNegative altitudes: {(df['baro_altitude'] < 0).sum()}")
print(f"\nZero velocity: {(df['velocity'] == 0).sum()}")
print(f"\nSample flight_number values (raw):")
print(df['flight_number'].head(10).tolist())

print("\n=== flight_routes table ===")
df2 = pd.read_sql_query("SELECT * FROM flight_routes", conn)
print(f"Total rows: {len(df2)}")
print(f"\nNull counts:")
print(df2.isnull().sum())
print(f"\nDuplicate flight_numbers: {df2['flight_number'].duplicated().sum()}")

conn.close()
