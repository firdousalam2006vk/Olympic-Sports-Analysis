"""
src/analyze.py
==============
Project: Global Olympic Sports Performance Analysis
Description: Conducts comprehensive exploratory and confirmatory data analysis
             across all historical Olympic editions (Summer 1896-2016, Winter 1924-2014).
             Calculates KPIs, country standings, sport dominance, gender evolution,
             host nation bump, continental efficiency, and capital investment ROI.
"""

import os
import json
import numpy as np
import pandas as pd

DATA_DIR = "data"
ATHLETES_PATH = os.path.join(DATA_DIR, "athletes.csv")
MEDALS_PATH = os.path.join(DATA_DIR, "medal_results.csv")
SUMMARY_OUTPUT_PATH = os.path.join(DATA_DIR, "analysis_summary.json")

def analyze_olympic_performance():
    print("=" * 75)
    print("GLOBAL OLYMPIC SPORTS PERFORMANCE ANALYSIS - ANALYTICAL AUDIT")
    print("=" * 75)
    
    # 1. Load Cleaned Datasets
    athletes_df = pd.read_csv(ATHLETES_PATH, low_memory=False)
    medals_df = pd.read_csv(MEDALS_PATH)
    
    results = {}
    
    # -------------------------------------------------------------
    # KPI Metrics
    # -------------------------------------------------------------
    total_editions = medals_df['games_id'].nunique()
    summer_editions = medals_df[medals_df['season'] == 'Summer']['games_id'].nunique()
    winter_editions = medals_df[medals_df['season'] == 'Winter']['games_id'].nunique()
    total_athletes = athletes_df['athlete_id'].nunique()
    total_participations = len(athletes_df)
    total_nocs = athletes_df['noc'].nunique()
    total_medals = medals_df['total_medals'].sum()
    total_gold = medals_df['gold'].sum()
    total_silver = medals_df['silver'].sum()
    total_bronze = medals_df['bronze'].sum()
    
    kpis = {
        "total_editions": int(total_editions),
        "summer_editions": int(summer_editions),
        "winter_editions": int(winter_editions),
        "unique_athletes": int(total_athletes),
        "total_event_participations": int(total_participations),
        "competing_nocs": int(total_nocs),
        "total_official_medals": int(total_medals),
        "total_gold": int(total_gold),
        "total_silver": int(total_silver),
        "total_bronze": int(total_bronze),
        "years_covered_summer": "1896 - 2016",
        "years_covered_winter": "1924 - 2014"
    }
    results["kpis"] = kpis
    
    print("\n--- 1. OVERALL OLYMPIC METRICS ---")
    for k, v in kpis.items():
        if isinstance(v, int):
            print(f"  {k.replace('_', ' ').title()}: {v:,}")
        else:
            print(f"  {k.replace('_', ' ').title()}: {v}")

    # -------------------------------------------------------------
    # All-Time Top 15 Country Medal Table
    # -------------------------------------------------------------
    top_nations = medals_df.groupby(['noc', 'country', 'continent']).agg(
        gold=('gold', 'sum'),
        silver=('silver', 'sum'),
        bronze=('bronze', 'sum'),
        total_medals=('total_medals', 'sum'),
        weighted_score=('weighted_score', 'sum'),
        athletes_entered=('athletes_count', 'sum')
    ).reset_index()
    
    top_nations['conversion_rate_pct'] = np.round(
        (top_nations['total_medals'] / top_nations['athletes_entered']) * 100, 2
    )
    
    top_15 = top_nations.sort_values(by=['gold', 'total_medals'], ascending=False).head(15)
    results["top_15_countries"] = top_15.to_dict(orient="records")
    
    print("\n--- 2. ALL-TIME TOP 15 COUNTRIES (BY GOLD & TOTAL MEDALS) ---")
    print(top_15[['country', 'gold', 'silver', 'bronze', 'total_medals', 'weighted_score', 'conversion_rate_pct']].to_string(index=False))

    # -------------------------------------------------------------
    # Longitudinal Participation & Gender Dynamics
    # -------------------------------------------------------------
    gender_trend = athletes_df.groupby(['year', 'season', 'sex']).agg(
        athletes=('athlete_id', 'nunique')
    ).unstack(fill_value=0).reset_index()
    gender_trend.columns = ['year', 'season', 'female', 'male']
    gender_trend['total'] = gender_trend['female'] + gender_trend['male']
    gender_trend['female_pct'] = np.round((gender_trend['female'] / gender_trend['total']) * 100, 2)
    
    summer_gender = gender_trend[gender_trend['season'] == 'Summer'].sort_values('year')
    results["gender_evolution_sample"] = summer_gender.tail(8).to_dict(orient="records")
    
    print("\n--- 3. SUMMER OLYMPICS GENDER EQUITY TRAJECTORY ---")
    print(summer_gender[['year', 'male', 'female', 'total', 'female_pct']].tail(8).to_string(index=False))

    # -------------------------------------------------------------
    # Top Sports by Medal Volume & Dominant Powers
    # -------------------------------------------------------------
    sport_medals = athletes_df[athletes_df['medal'] != 'No Medal'].drop_duplicates(
        subset=['year', 'season', 'sport', 'event', 'medal', 'noc']
    )
    top_sports = sport_medals['sport'].value_counts().head(10).reset_index()
    top_sports.columns = ['sport', 'total_medals']
    
    dominance = []
    for sp in top_sports['sport']:
        sp_df = sport_medals[sport_medals['sport'] == sp]
        top_nation = sp_df.groupby('country').size().sort_values(ascending=False).head(1)
        nation_name = top_nation.index[0]
        nation_medals = int(top_nation.values[0])
        total_sp_medals = len(sp_df)
        share = np.round((nation_medals / total_sp_medals) * 100, 1)
        dominance.append({
            "sport": sp,
            "total_medals": total_sp_medals,
            "dominant_country": nation_name,
            "dominant_country_medals": nation_medals,
            "dominance_share_pct": share
        })
    results["top_sports_dominance"] = dominance
    
    print("\n--- 4. TOP 10 SPORTS & HISTORIC DOMINANT NATIONS ---")
    print(pd.DataFrame(dominance).to_string(index=False))

    # -------------------------------------------------------------
    # The "Host Nation Advantage"
    # -------------------------------------------------------------
    summer_hosts = [
        (1952, "FIN", "Finland"), (1956, "AUS", "Australia"), (1960, "ITA", "Italy"),
        (1964, "JPN", "Japan"), (1968, "MEX", "Mexico"), (1976, "CAN", "Canada"),
        (1980, "URS", "Soviet Union"), (1988, "KOR", "South Korea"), (1992, "ESP", "Spain"),
        (1996, "USA", "United States"), (2000, "AUS", "Australia"), (2004, "GRE", "Greece"),
        (2008, "CHN", "China"), (2012, "GBR", "Great Britain"), (2016, "BRA", "Brazil")
    ]
    
    summer_years = sorted(medals_df[medals_df['season'] == 'Summer']['year'].unique())
    host_analysis = []
    
    for yr, noc, ctry in summer_hosts:
        idx = summer_years.index(yr)
        prev_yr = summer_years[idx-1]
        
        m_host = medals_df[(medals_df['noc'] == noc) & (medals_df['year'] == yr) & (medals_df['season'] == 'Summer')]
        m_pre = medals_df[(medals_df['noc'] == noc) & (medals_df['year'] == prev_yr) & (medals_df['season'] == 'Summer')]
        
        host_count = m_host['total_medals'].values[0] if len(m_host) > 0 else np.nan
        pre_count = m_pre['total_medals'].values[0] if len(m_pre) > 0 else np.nan
        
        if pd.notna(host_count) and pd.notna(pre_count):
            bump = host_count - pre_count
            pct = (bump / pre_count * 100) if pre_count > 0 else np.nan
            host_analysis.append({
                "host_year": yr, "country": ctry, "pre_medals": pre_count,
                "host_medals": host_count, "medal_bump": bump, "bump_pct": np.round(pct, 1)
            })
            
    df_ha = pd.DataFrame(host_analysis)
    pos_rate = (df_ha['medal_bump'] > 0).mean() * 100
    mean_bump = df_ha['medal_bump'].mean()
    median_bump = df_ha['medal_bump'].median()
    
    results["host_advantage"] = {
        "success_rate_pct": np.round(pos_rate, 1),
        "mean_bump": np.round(mean_bump, 1),
        "median_bump": np.round(median_bump, 1),
        "cases": df_ha.to_dict(orient="records")
    }
    
    print("\n--- 5. HOST NATION ADVANTAGE METRICS ---")
    print(f"  Host Editions Evaluated: {len(df_ha)}")
    print(f"  Positive Surge Rate: {pos_rate:.1f}%")
    print(f"  Average Net Medal Bump: +{mean_bump:.1f} medals")
    print(f"  Median Net Medal Bump: +{median_bump:.1f} medals")
    print("\nSample Host Nation Bumps:")
    print(df_ha.head(5).to_string(index=False))

    # -------------------------------------------------------------
    # Regional Continental Efficiency
    # -------------------------------------------------------------
    reg_summary = medals_df.groupby('continent').agg(
        total_athletes=('athletes_count', 'sum'),
        gold=('gold', 'sum'),
        total_medals=('total_medals', 'sum')
    ).reset_index()
    reg_summary['conversion_rate_pct'] = np.round(
        (reg_summary['total_medals'] / reg_summary['total_athletes']) * 100, 2
    )
    reg_clean = reg_summary[~reg_summary['continent'].isin(['Other', 'Special'])].sort_values('conversion_rate_pct', ascending=False)
    results["regional_efficiency"] = reg_clean.to_dict(orient="records")
    
    print("\n--- 6. REGIONAL SPORTS EFFICIENCY (CONVERSION RATE) ---")
    print(reg_clean[['continent', 'total_athletes', 'total_medals', 'conversion_rate_pct']].to_string(index=False))

    # Save summary JSON
    with open(SUMMARY_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[SUCCESS] Statistical audit saved to: {SUMMARY_OUTPUT_PATH}")

if __name__ == "__main__":
    analyze_olympic_performance()

