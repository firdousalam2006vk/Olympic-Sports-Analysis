# Olympic-Flask Web Portal
## Global Olympic Sports Performance Analysis Web Interface

A lightweight, high-performance Flask web portal providing interactive views and REST API endpoints for 120 years of Olympic performance data.

---

## 🚀 Quickstart Guide

### 1. Ensure Dependencies Are Installed
```bash
pip install flask pandas
```

### 2. Start the Local Server
```bash
cd Olympic-Flask
python app.py
```
*The application will launch locally at `http://127.0.0.1:5000`.*

---

## 🌐 Routes & Features
* `/` — **Executive Dashboard**: Top KPI badges (51 Editions, 230 Nations, 135k Athletes, 18,905 Medals), top 5 nations, and quick search.
* `/leaderboard` — **Interactive Leaderboard**: Search and filter nations across Summer, Winter, or All Seasons.
* `/host-advantage` — **Host Bump Analysis**: Benchmarking 15 host nations (+15.4 net medal surge, 86.7% success rate).
* `/funding-roi` — **Sports Funding ROI**: UK Sport lottery investment model ($r = 0.752$, £4.21M median cost/medal).
* `/dashboards` — **Tableau Public BI**: Direct embedded portal and cloud dashboard launcher.

---

## 🔌 REST API Endpoints
* `GET /api/kpis` — Returns global summary statistics (editions, medals, athletes, surge metrics).
* `GET /api/medals?country=USA&limit=10` — Returns filtered country medal tallies in JSON format.
* `GET /api/host-surge` — Returns host edition historical moving averages and net bumps.

---

## 🧪 Testing the Web App
Run the automated test suite verifying all routes:
```bash
python test_app.py
```
*Expected Result: 8 of 8 tests pass with HTTP 200 OK.*

