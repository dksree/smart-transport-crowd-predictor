from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import random
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from dataset import (
    generate_dataset, get_crowd_level, get_crowd_color,
    predict_crowd, simulate_bus_data, STATIONS, BUSES
)

app = Flask(__name__)
CORS(app)

# Generate dataset on startup
CSV_PATH = os.path.join(os.path.dirname(__file__), "crowd_data.csv")
if not os.path.exists(CSV_PATH):
    df = generate_dataset()
    df.to_csv(CSV_PATH, index=False)
else:
    df = pd.read_csv(CSV_PATH)

# ─── API: Current crowd levels for all stations ───────────────────────────────
@app.route("/crowd", methods=["GET"])
def get_crowd():
    station = request.args.get("station")
    now = datetime.now()
    hour = int(request.args.get("hour", now.hour))
    day = int(request.args.get("day", now.weekday()))

    results = []
    stations = [station] if station else STATIONS
    for s in stations:
        count = predict_crowd(s, hour, day, df)
        noise = random.randint(-20, 20)
        count = max(10, count + noise)
        level = get_crowd_level(count)
        results.append({
            "station": s,
            "crowd_count": count,
            "crowd_level": level,
            "color": get_crowd_color(level),
            "hour": hour,
            "capacity": 600,
            "capacity_pct": min(100, int((count / 600) * 100))
        })
    return jsonify({"status": "ok", "data": results, "timestamp": now.isoformat()})


# ─── API: Predicted crowd for next 12 hours ───────────────────────────────────
@app.route("/predict", methods=["GET"])
def predict():
    station = request.args.get("station", STATIONS[0])
    day = int(request.args.get("day", datetime.now().weekday()))

    predictions = []
    for h in range(6, 24):
        count = predict_crowd(station, h, day, df)
        level = get_crowd_level(count)
        predictions.append({
            "hour": h,
            "hour_label": f"{h:02d}:00",
            "predicted_count": count,
            "crowd_level": level,
            "color": get_crowd_color(level)
        })

    peak_hour = max(predictions, key=lambda x: x["predicted_count"])
    return jsonify({
        "status": "ok",
        "station": station,
        "predictions": predictions,
        "peak_hour": peak_hour["hour_label"],
        "peak_count": peak_hour["predicted_count"]
    })


# ─── API: Bus tracking data ───────────────────────────────────────────────────
@app.route("/bus", methods=["GET"])
def get_buses():
    buses = simulate_bus_data()
    return jsonify({"status": "ok", "buses": buses, "total": len(buses)})


# ─── API: Analytics — hourly average across all stations ─────────────────────
@app.route("/analytics", methods=["GET"])
def analytics():
    hourly = df.groupby("hour")["crowd_count"].mean().reset_index()
    hourly_data = [
        {"hour": f"{int(row.hour):02d}:00", "avg_crowd": int(row.crowd_count)}
        for _, row in hourly.iterrows()
    ]
    station_avg = df.groupby("station_name")["crowd_count"].mean().reset_index()
    station_data = [
        {"station": row.station_name, "avg_crowd": int(row.crowd_count)}
        for _, row in station_avg.iterrows()
    ]
    return jsonify({
        "status": "ok",
        "hourly_trend": hourly_data,
        "station_comparison": station_data,
        "total_records": len(df)
    })


# ─── API: Stations list ───────────────────────────────────────────────────────
@app.route("/stations", methods=["GET"])
def get_stations():
    return jsonify({"stations": STATIONS})


if __name__ == "__main__":
    print("🚌 Smart Transport Crowd Predictor API starting...")
    print("📡 Running on http://localhost:5000")
    app.run(debug=True, port=5000)
