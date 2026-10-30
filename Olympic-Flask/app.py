"""
Olympic-Flask/app.py
===================
Interactive Flask Web Application for Global Olympic Sports Performance Analysis.
Serves interactive dashboards, search/filter APIs, and business intelligence views.
"""

import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MEDALS_CSV = os.path.join(DATA_DIR, "medal_results.csv")
HOST_CSV = os.path.join(DATA_DIR, "host_nation_performance.csv")
FUNDING_CSV = os.path.join(DATA_DIR, "sports_funding_benchmark.csv")
SUMMARY_JSON = os.path.join(DATA_DIR, "analysis_summary.json")

TABLEAU_PUBLIC_URL = "https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3"
GITHUB_REPO_URL = "https://github.com/firdousalam2006vk/Olympic-Sports-Analysis"

# In-memory cached dataframes
_df_medals = None
_df_host = None
_df_fund = None

def get_medals_df():
    global _df_medals
    if _df_medals is None and os.path.exists(MEDALS_CSV):
        _df_medals = pd.read_csv(MEDALS_CSV)
    return _df_medals

def get_host_df():
    global _df_host
    if _df_host is None and os.path.exists(HOST_CSV):
        _df_host = pd.read_csv(HOST_CSV)
    return _df_host

def get_fund_df():
    global _df_fund
    if _df_fund is None and os.path.exists(FUNDING_CSV):
        _df_fund = pd.read_csv(FUNDING_CSV)
    return _df_fund

@app.context_processor
def inject_global_vars():
    return {
        "tableau_url": TABLEAU_PUBLIC_URL,
        "github_url": GITHUB_REPO_URL,
        "author_name": "Md. Firdous Alam"
    }

@app.route("/")
def index():
    df = get_medals_df()
    kpis = {
        "editions": df["games_id"].nunique() if df is not None else 51,
        "nations": df["noc"].nunique() if df is not None else 230,
        "athletes": "135,571",
        "total_medals": int(df["total_medals"].sum()) if df is not None else 18905,
        "gold_medals": int(df["gold"].sum()) if df is not None else 6195,
        "host_bump": "+15.4 Medals (86.7% Surge Rate)"
    }
    
    # Top 5 Nations for quick preview
    top_5 = []
    if df is not None:
        agg = df.groupby(["noc", "country"])[["gold", "silver", "bronze", "total_medals"]].sum().reset_index()
        top_5 = agg.sort_values(by="total_medals", ascending=False).head(5).to_dict(orient="records")

    return render_template("index.html", kpis=kpis, top_5=top_5)

@app.route("/leaderboard")
def leaderboard():
    df = get_medals_df()
    season = request.args.get("season", "All")
    search = request.args.get("q", "").strip().lower()

    if df is not None:
        filtered = df.copy()
        if season in ["Summer", "Winter"]:
            filtered = filtered[filtered["season"] == season]
        
        agg = filtered.groupby(["noc", "country"])[["gold", "silver", "bronze", "total_medals", "weighted_score"]].sum().reset_index()
        
        if search:
            agg = agg[agg["country"].str.lower().str.contains(search, na=False) | agg["noc"].str.lower().str.contains(search, na=False)]
            
        agg = agg.sort_values(by="total_medals", ascending=False)
        records = agg.head(100).to_dict(orient="records")
    else:
        records = []

    return render_template("leaderboard.html", records=records, current_season=season, search_query=search)

@app.route("/host-advantage")
def host_advantage():
    df_h = get_host_df()
    hosts = []
    if df_h is not None:
        hosts = df_h.to_dict(orient="records")
    return render_template("host_advantage.html", hosts=hosts)

@app.route("/funding-roi")
def funding_roi():
    df_f = get_fund_df()
    fund_records = []
    if df_f is not None:
        fund_records = df_f.to_dict(orient="records")
    return render_template("funding_roi.html", records=fund_records)

@app.route("/dashboards")
def dashboards():
    return render_template("dashboards.html")

# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------
@app.route("/api/kpis")
def api_kpis():
    df = get_medals_df()
    if df is None:
        return jsonify({"error": "Dataset not available"}), 500
    return jsonify({
        "total_editions": int(df["games_id"].nunique()),
        "total_nations": int(df["noc"].nunique()),
        "total_medals": int(df["total_medals"].sum()),
        "total_gold": int(df["gold"].sum()),
        "total_silver": int(df["silver"].sum()),
        "total_bronze": int(df["bronze"].sum()),
        "host_bump_avg": 15.4,
        "host_surge_rate_pct": 86.7
    })

@app.route("/api/medals")
def api_medals():
    df = get_medals_df()
    if df is None:
        return jsonify([]), 500
    
    country = request.args.get("country", "")
    limit = int(request.args.get("limit", 20))
    
    filtered = df
    if country:
        filtered = filtered[filtered["country"].str.contains(country, case=False, na=False) | (filtered["noc"] == country.upper())]
        
    agg = filtered.groupby(["noc", "country"])[["gold", "silver", "bronze", "total_medals"]].sum().reset_index()
    agg = agg.sort_values(by="total_medals", ascending=False).head(limit)
    return jsonify(agg.to_dict(orient="records"))

@app.route("/api/host-surge")
def api_host_surge():
    df_h = get_host_df()
    if df_h is None:
        return jsonify([]), 500
    return jsonify(df_h.to_dict(orient="records"))

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  OLYMPIC SPORTS PERFORMANCE ANALYSIS - FLASK WEB PORTAL")
    print("  Running locally at: http://127.0.0.1:5000")
    print("  Author: Md. Firdous Alam | Skills Wallet Capstone Project")
    print("="*70 + "\n")
    app.run(debug=True, port=5000)

