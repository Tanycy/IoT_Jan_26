import sqlite3
import requests
import time
import csv
import os

DB = "perak_flights.db"
AERODATABOX_KEY = "cmmiy02ky0001kz04cf0vj4md"

# ── Airport lookup ────────────────────────────────────────────────────────
AIRPORT_LOOKUP = {}
CITY_LOOKUP = {}

def load_airports():
    csv_path = "airports.csv"
    if not os.path.exists(csv_path):
        print("Downloading airports.csv...")
        r = requests.get("https://ourairports.com/data/airports.csv", timeout=30)
        with open(csv_path, "wb") as f:
            f.write(r.content)
        print("Downloaded.")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            icao = row.get("icao_code", "").strip()
            if icao:
                AIRPORT_LOOKUP[icao] = row.get("name", icao)
                CITY_LOOKUP[icao]    = row.get("municipality", "")

def icao_to_name(icao_code):
    if not icao_code:
        return "Unknown"
    name = AIRPORT_LOOKUP.get(icao_code, "")
    city = CITY_LOOKUP.get(icao_code, "")
    if name:
        return f"{city} - {name}" if city else name
    return icao_code

# ── Airline hub fallback ──────────────────────────────────────────────────
AIRLINE_HUB = {
    "BAW": ("EGLL", "London - London Heathrow Airport"),
    "MAS": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),
    "AXM": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),
    "THY": ("LTFM", "Istanbul - Istanbul Airport"),
    "SIA": ("WSSS", "Singapore - Singapore Changi Airport"),
    "UAE": ("OMDB", "Dubai - Dubai International Airport"),
    "ETD": ("OMAA", "Abu Dhabi - Abu Dhabi International Airport"),
    "QTR": ("OTBH", "Doha - Hamad International Airport"),
    "CPA": ("VHHH", "Hong Kong - Hong Kong International Airport"),
    "CES": ("ZSPD", "Shanghai - Shanghai Pudong International Airport"),
    "CSN": ("ZGGG", "Guangzhou - Guangzhou Baiyun International Airport"),
    "CCA": ("ZBAA", "Beijing - Beijing Capital International Airport"),
    "JAL": ("RJTT", "Tokyo - Tokyo Haneda Airport"),
    "ANA": ("RJTT", "Tokyo - Tokyo Haneda Airport"),
    "KAL": ("RKSI", "Incheon - Incheon International Airport"),
    "AAR": ("RKSI", "Incheon - Incheon International Airport"),
    "THA": ("VTBS", "Bangkok - Suvarnabhumi Airport"),
    "FDX": ("KMEM", "Memphis - Memphis International Airport"),
    "UPS": ("KSDF", "Louisville - Louisville International Airport"),
    "IGO": ("VIDP", "Delhi - Indira Gandhi International Airport"),
    "AIC": ("VIDP", "Delhi - Indira Gandhi International Airport"),
    "BBC": ("VGHS", "Dhaka - Hazrat Shahjalal International Airport"),
    "TGW": ("WSSS", "Singapore - Singapore Changi Airport"),
    "QFA": ("YSSY", "Sydney - Sydney Kingsford Smith International Airport"),
    "KLM": ("EHAM", "Amsterdam - Amsterdam Airport Schiphol"),
    "DLH": ("EDDF", "Frankfurt - Frankfurt Airport"),
    "AFR": ("LFPG", "Paris - Charles de Gaulle Airport"),
    # Malaysia / Indonesia / Southeast Asia
    "MXD": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),  # Batik Air Malaysia
    "BTK": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),  # Batik Air
    "XAX": ("WIII", "Jakarta - Soekarno-Hatta International Airport"),     # Xpress Air
    "AWQ": ("WIII", "Jakarta - Soekarno-Hatta International Airport"),     # Aero Wisata
    "LNI": ("WIII", "Jakarta - Soekarno-Hatta International Airport"),     # Lion Air
    "IDX": ("WIII", "Jakarta - Soekarno-Hatta International Airport"),     # Indonesia AirAsia
    "GIA": ("WIII", "Jakarta - Soekarno-Hatta International Airport"),     # Garuda Indonesia
    "SJY": ("WIII", "Jakarta - Soekarno-Hatta International Airport"),     # Sriwijaya Air
    "WON": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),  # Firefly
    "FAX": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),  # Firefly (alt)
    "MYS": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),  # Malaysia misc
    "HGB": ("WMKP", "Penang - Penang International Airport"),              # Heli misc
    "PAC": ("RPLL", "Manila - Ninoy Aquino International Airport"),        # Philippine Airlines
    "PAL": ("RPLL", "Manila - Ninoy Aquino International Airport"),        # Philippine Airlines
    "CEB": ("RPLL", "Manila - Ninoy Aquino International Airport"),        # Cebu Pacific
    "VJC": ("VVTS", "Ho Chi Minh City - Tan Son Nhat International Airport"), # VietJet
    "HVN": ("VVNB", "Hanoi - Noi Bai International Airport"),             # Vietnam Airlines
    "BAV": ("VVNB", "Hanoi - Noi Bai International Airport"),             # Bamboo Airways
    "MHV": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),  # Malindo misc
    "RBA": ("WBSB", "Bandar Seri Begawan - Brunei International Airport"), # Royal Brunei
    # Added from not-found list
    "AFL": ("UUEE", "Moscow - Sheremetyevo International Airport"),         # Aeroflot
    "AIQ": ("VTCC", "Chiang Mai - Chiang Mai International Airport"),       # AirAsia Thailand
    "ALK": ("VCBI", "Colombo - Bandaranaike International Airport"),        # SriLankan Airlines
    "AYG": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),   # Malaysia misc
    "AZG": ("EGLL", "London - London Heathrow Airport"),                    # UK misc
    "CAL": ("RCTP", "Taipei - Taiwan Taoyuan International Airport"),       # China Airlines
    "CLX": ("ELLX", "Luxembourg - Luxembourg Airport"),                     # Cargolux
    "EXC": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),   # Execair Malaysia
    "FFM": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),   # Firefly Malaysia
    "FIN": ("EFHK", "Helsinki - Helsinki Vantaa Airport"),                  # Finnair
    "JST": ("YSSY", "Sydney - Sydney Kingsford Smith International Airport"), # Jetstar
    "KXP": ("WMKK", "Kuala Lumpur - Kuala Lumpur International Airport"),   # KL misc
    "MMA": ("VYYY", "Yangon - Yangon International Airport"),               # Myanmar Airways
}

def airline_hub_fallback(callsign):
    prefix = callsign[:3].upper()
    if prefix in AIRLINE_HUB:
        icao, name = AIRLINE_HUB[prefix]
        return icao, name
    return None, None

# ── 1. OpenSky ────────────────────────────────────────────────────────────
def lookup_opensky(callsign):
    try:
        r = requests.get(
            "https://opensky-network.org/api/routes",
            params={"callsign": callsign}, timeout=10
        )
        if r.status_code == 200:
            route = r.json().get("route", [])
            if len(route) >= 2:
                return route[0], route[-1]
    except Exception as e:
        print(f"  OpenSky error: {e}")
    return None, None

# ── 2. AeroDataBox ────────────────────────────────────────────────────────
def lookup_aerodatabox(callsign):
    try:
        url = f"https://aerodatabox.p.rapidapi.com/flights/callsign/{callsign}"
        headers = {
            "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
            "X-RapidAPI-Key":  AERODATABOX_KEY
        }
        r = requests.get(url, headers=headers, timeout=10)
        print(f"  AeroDataBox status: {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            flights = data if isinstance(data, list) else [data]
            if len(flights) == 0:
                return None, None, None, None

            flight   = flights[0]
            dep      = flight.get("departure", {})
            arr      = flight.get("arrival", {})
            dep_icao = dep.get("airport", {}).get("icao")
            arr_icao = arr.get("airport", {}).get("icao")
            dep_name = dep.get("airport", {}).get("name", dep_icao)
            arr_name = arr.get("airport", {}).get("name", arr_icao)

            if dep_icao:
                print(f"  AeroDataBox found: {dep_icao} -> {arr_icao}")
                return dep_icao, arr_icao, dep_name, arr_name

    except Exception as e:
        print(f"  AeroDataBox error: {e}")
    return None, None, None, None

# ── Combined 3-layer lookup ───────────────────────────────────────────────
def lookup_route(callsign):
    callsign = callsign.strip()

    # Layer 1: OpenSky
    dep_icao, arr_icao = lookup_opensky(callsign)
    if dep_icao:
        print(f"  [OpenSky] {dep_icao} -> {arr_icao}")
        return dep_icao, arr_icao, icao_to_name(dep_icao), icao_to_name(arr_icao), "opensky"

    # Layer 2: AeroDataBox
    dep_icao, arr_icao, dep_name, arr_name = lookup_aerodatabox(callsign)
    if dep_icao:
        local_dep = icao_to_name(dep_icao)
        local_arr = icao_to_name(arr_icao) if arr_icao else arr_name
        return (
            dep_icao, arr_icao,
            local_dep if local_dep != dep_icao else dep_name,
            local_arr if local_arr != arr_icao else arr_name,
            "aerodatabox"
        )

    # Layer 3: Hub fallback
    dep_icao, dep_name = airline_hub_fallback(callsign)
    if dep_icao:
        print(f"  [Hub fallback] {dep_icao} = {dep_name}")
        return dep_icao, None, dep_name, None, "hub_fallback"

    return None, None, None, None, None

# ── Main ──────────────────────────────────────────────────────────────────
def fetch_routes():
    load_airports()
    print("Airports loaded.\n")

    conn = sqlite3.connect(DB)
    c    = conn.cursor()

    # Create table fresh with source column
    c.execute("""
        CREATE TABLE IF NOT EXISTS flight_routes (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            icao24            TEXT,
            flight_number     TEXT,
            departure_airport TEXT,
            arrival_airport   TEXT,
            departure_icao    TEXT,
            arrival_icao      TEXT,
            source            TEXT,
            timestamp         TEXT
        )
    """)

    # Add source column if it's missing from old table
    try:
        c.execute("ALTER TABLE flight_routes ADD COLUMN source TEXT")
        print("Added missing 'source' column to existing table.")
    except sqlite3.OperationalError:
        pass  # Column already exists, that's fine

    conn.commit()

    # Skip already-fetched flights
    c.execute("SELECT flight_number FROM flight_routes")
    already_done = set(row[0] for row in c.fetchall())
    print(f"Already saved: {len(already_done)} flights, skipping those.\n")

    c.execute("""
        SELECT DISTINCT TRIM(flight_number), icao24
        FROM flights
        WHERE flight_number IS NOT NULL
          AND TRIM(flight_number) != ''
    """)
    flights = [f for f in c.fetchall() if f[0] not in already_done]
    print(f"Remaining to look up: {len(flights)} flights.\n")

    opensky_hits     = 0
    aerodatabox_hits = 0
    hub_hits         = 0
    not_found        = 0

    for i, (flight_number, icao24) in enumerate(flights):
        print(f"[{i+1}/{len(flights)}] {flight_number} ...")

        dep_icao, arr_icao, dep_name, arr_name, source = lookup_route(flight_number)

        if not dep_icao:
            print(f"  Not found.\n")
            not_found += 1
            time.sleep(0.3)
            continue

        if source == "opensky":        opensky_hits += 1
        elif source == "aerodatabox":  aerodatabox_hits += 1
        else:                          hub_hits += 1

        c.execute("""
            INSERT INTO flight_routes
            (icao24, flight_number, departure_airport, arrival_airport,
             departure_icao, arrival_icao, source, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            icao24, flight_number,
            dep_name, arr_name or "Unknown",
            dep_icao, arr_icao or "",
            source
        ))
        conn.commit()
        time.sleep(0.3)

    conn.close()
    print(f"""
==========================================
Done!
  OpenSky exact routes  : {opensky_hits}
  AeroDataBox routes    : {aerodatabox_hits}
  Airline hub fallback  : {hub_hits}
  Not found             : {not_found}
  Total saved           : {opensky_hits + aerodatabox_hits + hub_hits}
==========================================
""")

if __name__ == "__main__":
    fetch_routes()
