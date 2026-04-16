import pandas as pd
import numpy as np
import json

# Stations list
STATIONS = [
    "Central Station", "Airport Terminal", "City Mall",
    "University Hub", "Tech Park", "Old Town", "Stadium Gate", "Market Square"
]

BUSES = [
    {"id": "BUS-101", "route": "Central → Airport", "stops": ["Central Station", "City Mall", "Airport Terminal"]},
    {"id": "BUS-202", "route": "University → Tech Park", "stops": ["University Hub", "Market Square", "Tech Park"]},
    {"id": "BUS-303", "route": "Old Town → Stadium", "stops": ["Old Town", "Central Station", "Stadium Gate"]},
    {"id": "BUS-404", "route": "Market → University", "stops": ["Market Square", "City Mall", "University Hub"]},
]

def generate_dataset():
    rows = []
    for station in STATIONS:
        for hour in range(6, 24):
            for day in range(7):
                # Simulate realistic crowd patterns
                base = 200
                if hour in [8, 9]:       base += 350  # morning peak
                elif hour in [17, 18, 19]: base += 400  # evening peak
                elif hour in [12, 13]:    base += 150  # lunch rush
                elif hour < 7 or hour > 21: base -= 100
                if day >= 5: base = int(base * 0.65)  # weekend dip

                noise = np.random.randint(-40, 40)
                crowd = max(10, base + noise)
                tickets = int(crowd * np.random.uniform(0.6, 0.9))
                rows.append({
                    "station_name": station,
                    "day_of_week": day,
                    "hour": hour,
                    "crowd_count": crowd,
                    "tickets_sold": tickets
                })
    df = pd.DataFrame(rows)
    df.to_csv("crowd_data.csv", index=False)
    return df

def get_crowd_level(count):
    if count < 150: return "Low"
    elif count < 300: return "Medium"
    else: return "High"

def get_crowd_color(level):
    return {"Low": "#00d4aa", "Medium": "#f5a623", "High": "#e74c3c"}[level]

def predict_crowd(station, hour, day_of_week, df):
    subset = df[(df["station_name"] == station) & (df["hour"] == hour) & (df["day_of_week"] == day_of_week)]
    if subset.empty:
        return 200
    return int(subset["crowd_count"].mean())

def simulate_bus_data():
    import random, datetime
    buses = []
    for b in BUSES:
        occ = random.randint(20, 95)
        eta = random.randint(1, 15)
        buses.append({
            "id": b["id"],
            "route": b["route"],
            "stops": b["stops"],
            "occupancy_pct": occ,
            "seats_filled": f"{occ}%",
            "eta_minutes": eta,
            "next_arrival": f"{eta} min",
            "status": "On Time" if eta < 10 else "Delayed",
            "lat": 17.385 + random.uniform(-0.05, 0.05),
            "lng": 78.486 + random.uniform(-0.05, 0.05)
        })
    return buses
