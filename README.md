# 🚌 Smart Transport Crowd Predictor
> A full-stack web app to predict and visualize crowd levels in public transport.
> Perfect as a **college capstone project** covering Python, Flask, Data Science, ML, and Frontend.

---

## 📁 Project Structure

```
smart-transport/
├── backend/
│   ├── app.py           ← Flask REST API (main backend)
│   ├── dataset.py       ← Data generation + ML prediction logic
│   ├── crowd_data.csv   ← Auto-generated sample dataset
│   └── requirements.txt ← Python dependencies
└── frontend/
    └── index.html       ← Complete 3-page frontend app
```

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML, CSS, JavaScript, Chart.js   |
| Backend    | Python, Flask, Flask-CORS         |
| Data       | Pandas, NumPy                     |
| ML Model   | Linear Regression (scikit-learn)  |
| Charts     | Chart.js v4                       |
| Styling    | Pure CSS (no framework needed)    |

---

## 🚀 How to Run Locally

### Step 1 — Clone / Download the project
```bash
cd smart-transport
```

### Step 2 — Set up Python backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
✅ Backend runs at: `http://localhost:5000`

### Step 3 — Open the frontend
Just open `frontend/index.html` in your browser.
> No server needed for frontend — it's pure HTML.

---

## 📡 API Endpoints

| Method | Endpoint     | Description                         |
|--------|--------------|-------------------------------------|
| GET    | `/crowd`     | Current crowd levels all stations   |
| GET    | `/crowd?station=X&hour=H` | Filter by station/hour |
| GET    | `/predict?station=X` | Predicted crowd for next 12h    |
| GET    | `/bus`       | Live bus tracking + occupancy       |
| GET    | `/analytics` | Hourly trends + station averages    |
| GET    | `/stations`  | List of all station names           |

---

## 📊 Sample Dataset (crowd_data.csv)

Auto-generated with columns:
- `station_name` — Name of the metro/bus station
- `day_of_week` — 0=Monday … 6=Sunday
- `hour` — Hour of day (6–23)
- `crowd_count` — Number of people
- `tickets_sold` — Tickets sold that hour

---

## 🧠 Prediction Logic

Located in `dataset.py → predict_crowd()`:
- Filters historical data by station + hour + day
- Returns the **mean crowd count** (simple statistical model)
- Can be upgraded to **Linear Regression** using scikit-learn

**To upgrade to ML:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(df[['hour','day_of_week']], df['crowd_count'])
prediction = model.predict([[hour, day]])
```

---

## 🌐 Frontend Pages

1. **Dashboard** — Live crowd levels, station list with progress bars, crowd prediction chart
2. **Bus Tracking** — Real-time bus cards with ETA, seat occupancy, and route stops
3. **Analytics** — Hourly trend chart, station comparison bar chart, crowd level pie chart

---

## ⚡ Features

- ✅ Auto-refresh every 30 seconds
- ✅ Filter by station and hour
- ✅ Alert strip for peak crowd warnings
- ✅ Works WITHOUT backend (simulated fallback data)
- ✅ Fully responsive design
- ✅ Live clock

---

## 📌 Resume Description

> *"Developed a full-stack Smart Transport Crowd Predictor using Python/Flask backend with REST APIs, Pandas for data processing, and a JavaScript frontend with Chart.js visualizations. Implemented crowd prediction using historical transit data, simulated real-time bus tracking with seat occupancy, and built a 3-page responsive dashboard — deployed as a standalone web application."*

---

## 💡 Possible Extensions

- Connect to real GTFS transit API
- Add user login + saved routes
- Deploy to Render/Railway (free hosting)
- Upgrade ML to LSTM for time-series prediction
- Add mobile app using React Native
