"""
Script 03: Comprehensive Exploratory Data Analysis & Metric Validation
=====================================================================
Project: Global Olympic Sports Performance Analysis
Author: Senior Data Analyst & Tableau Developer
Description: Performs deep statistical analysis across country rankings,
             gender evolution, seasonal growth, sport dominance,
             host nation bump, continental efficiency, and investment ROI.
"""

import os
import json
import numpy as np
import pandas as pd

PROCESSED_DIR = os.path.join("data", "processed")
OUTPUT_STATS_PATH = os.path.join("data", "processed", "analysis_summary.json")

def run_analysis():
    print("=" * 70)
    print("GLOBAL OLYMPIC SPORTS PERFORMANCE ANALYSIS - STATISTICAL AUDIT")
    print("=" * 70)
    
    # Load processed datasets
    athletes_df = pd.read_csv(os.path.join(PROCESSED_DIR, "athletes.csv"), low_memory=False)
    medals_df = pd.read_csv(os.path.join(PROCESSED_DIR, "medal_results.csv"))
    host_df = pd.read_csv(os.path.join(PROCESSED_DIR, "host_nation_performance.csv"))
    reg_df = pd.read_csv(os.path.join(PROCESSED_DIR, "regional_sports_efficiency.csv"))
    funding_df = pd.read_csv(os.path.join(PROCESSED_DIR, "sports_funding_benchmark.csv"))
    
    summary = {}
    
    # -------------------------------------------------------------
    # 1. Overall Olympic KPIs
    # -------------------------------------------------------------
    total_editions = medals_df['games_id'].nunique()
    summer_editions = medals_df[medals_df['season'] == 'Summer']['games_id'].nunique()
    winter_editions = medals_df[medals_df['season'] == 'Winter']['games_id'].nunique()
    total_athletes = athletes_df['athlete_id'].nunique()
    total_participations = len(athletes_df)
    total_nocs = athletes_df['noc'].nunique()
    total_official_medals = medals_df['total_medals'].sum()
    total_gold = medals_df['gold'].sum()
    total_silver = medals_df['silver'].sum()
    total_bronze = medals_df['bronze'].sum()
    
    kpis = {
        "total_editions": int(total_editions),
        "summer_editions": int(summer_editions),
        "winter_editions": int(winter_editions),
        "total_unique_athletes": int(total_athletes),
        "total_athlete_events": int(total_participations),
        "total_unique_nocs": int(total_nocs),
        "total_official_medals": int(total_official_medals),
        "total_gold": int(total_gold),
        "total_silver": int(total_silver),
        "total_bronze": int(total_bronze)
    }
    summary["kpis"] = kpis
    
    print("\n--- 1. OVERALL OLYMPIC METRICS ---")
    for k, v in kpis.items():
        print(f"  {k.replace('_', ' ').title()}: {v:,}")
        
    # -------------------------------------------------------------
    # 2. All-Time Top 15 Country Medal Table
    # -------------------------------------------------------------
    top_countries = medals_df.groupby(['noc', 'country', 'continent']).agg(
        gold=('gold', 'sum'),
        silver=('silver', 'sum'),
        bronze=('bronze', 'sum'),
        total_medals=('total_medals', 'sum'),
        weighted_score=('weighted_score', 'sum'),
        total_athletes=('athletes_count', 'sum')
    ).reset_index()
    
    top_countries['medal_efficiency'] = np.round(
        (top_countries['total_medals'] / top_countries['total_athletes']) * 100, 2
    )
    top_15 = top_countries.sort_values(by=['gold', 'total_medals'], ascending=False).head(15)
    summary["top_15_countries"] = top_15.to_dict(orient="records")
    
    print("\n--- 2. ALL-TIME TOP 15 COUNTRIES (BY GOLD & TOTAL MEDALS) ---")
    print(top_15[['country', 'gold', 'silver', 'bronze', 'total_medals', 'weighted_score', 'medal_efficiency']].to_string(index=False))

    # -------------------------------------------------------------
    # 3. Longitudinal Athlete Participation & Gender Dynamics
    # -------------------------------------------------------------
    gender_trend = athletes_df.groupby(['year', 'season', 'sex']).agg(
        unique_athletes=('athlete_id', 'nunique')
    ).unstack(fill_value=0).reset_index()
    gender_trend.columns = ['year', 'season', 'female_athletes', 'male_athletes']
    gender_trend['total_athletes'] = gender_trend['female_athletes'] + gender_trend['male_athletes']
    gender_trend['female_share_pct'] = np.round(
        (gender_trend['female_athletes'] / gender_trend['total_athletes']) * 100, 2
    )
    
    # Modern Summer trajectory
    summer_gender = gender_trend[gender_trend['season'] == 'Summer'].sort_values('year')
    summary["gender_trajectory_summer_sample"] = summer_gender.tail(10).to_dict(orient="records")
    
    print("\n--- 3. RECENT SUMMER OLYMPICS GENDER PARTICIPATION TREND ---")
    print(summer_gender[['year', 'male_athletes', 'female_athletes', 'total_athletes', 'female_share_pct']].tail(8).to_string(index=False))

    # -------------------------------------------------------------
    # 4. Top Sports by Medal Volume & Country Dominance
    # -------------------------------------------------------------
    sport_medals = athletes_df[athletes_df['medal'] != 'No Medal'].drop_duplicates(
        subset=['year', 'season', 'sport', 'event', 'medal', 'noc']
    )
    sport_volume = sport_medals.groupby('sport').agg(
        total_medals=('medal', 'count'),
        unique_countries=('noc', 'nunique')
    ).sort_values('total_medals', ascending=False).head(15).reset_index()
    
    # Dominant nation per top sport
    top_sports_list = sport_volume['sport'].tolist()
    dominance = []
    for sp in top_sports_list[:10]:
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
    summary["sport_dominance"] = dominance
    
    print("\n--- 4. TOP 10 SPORTS & HISTORIC DOMINANT NATIONS ---")
    print(pd.DataFrame(dominance).to_string(index=False))

    # -------------------------------------------------------------
    # 5. Host Nation Advantage (Host Bump Validation)
    # -------------------------------------------------------------
    valid_host_bumps = host_df[host_df['medal_bump'].notna()]
    mean_bump = valid_host_bumps['medal_bump'].mean()
    median_bump = valid_host_bumps['medal_bump'].median()
    positive_bumps = (valid_host_bumps['medal_bump'] > 0).sum()
    total_valid = len(valid_host_bumps)
    win_rate = (positive_bumps / total_valid) * 100
    
    host_summary = {
        "valid_host_samples": int(total_valid),
        "nations_with_positive_bump": int(positive_bumps),
        "host_bump_success_rate_pct": np.round(win_rate, 1),
        "mean_medal_bump": np.round(mean_bump, 2),
        "median_medal_bump": np.round(median_bump, 2),
        "top_bump_cases": valid_host_bumps.sort_values('medal_bump', ascending=False)[
            ['host_year', 'country', 'pre_medals', 'host_medals', 'medal_bump', 'medal_bump_pct']
        ].head(5).to_dict(orient="records")
    }
    summary["host_advantage"] = host_summary
    
    print("\n--- 5. HOST NATION ADVANTAGE METRICS ---")
    print(f"  Sample Host Editions Analyzed: {total_valid}")
    print(f"  Nations with Increased Medals: {positive_bumps} of {total_valid} ({win_rate:.1f}%)")
    print(f"  Average Medal Bump: +{mean_bump:.1f} medals")
    print(f"  Median Medal Bump: +{median_bump:.1f} medals")
    print("\nTop 5 Host Nation Bumps:")
    print(pd.DataFrame(host_summary["top_bump_cases"]).to_string(index=False))

    # -------------------------------------------------------------
    # 6. Regional Sports Efficiency Analysis
    # -------------------------------------------------------------
    print("\n--- 6. REGIONAL SPORTS EFFICIENCY BENCHMARKS ---")
    print(reg_df[['continent', 'total_athlete_participations', 'total_gold', 'total_medals', 'medals_per_100_athletes', 'gold_share_pct']].to_string(index=False))
    summary["regional_efficiency"] = reg_df.to_dict(orient="records")

    # -------------------------------------------------------------
    # 7. High-Performance Investment ROI (UK Sport Benchmark)
    # -------------------------------------------------------------
    rio_funding = funding_df[funding_df['cycle'] == 'Rio 2016']
    corr_rio = np.corrcoef(rio_funding['funding_millions_gbp'], rio_funding['medals_won'])[0, 1]
    
    mean_cost_per_medal = rio_funding['cost_per_medal_millions_gbp'].mean()
    median_cost_per_medal = rio_funding['cost_per_medal_millions_gbp'].median()
    
    investment_summary = {
        "correlation_funding_vs_medals": np.round(corr_rio, 3),
        "mean_cost_per_medal_gbp_m": np.round(mean_cost_per_medal, 2),
        "median_cost_per_medal_gbp_m": np.round(median_cost_per_medal, 2),
        "most_efficient_sports": rio_funding.sort_values('cost_per_medal_millions_gbp').dropna().head(4)[
            ['sport', 'funding_millions_gbp', 'medals_won', 'cost_per_medal_millions_gbp']
        ].to_dict(orient="records"),
        "least_efficient_funded_sports": rio_funding.sort_values('cost_per_medal_millions_gbp', ascending=False).dropna().head(4)[
            ['sport', 'funding_millions_gbp', 'medals_won', 'cost_per_medal_millions_gbp']
        ].to_dict(orient="records")
    }
    summary["investment_analysis"] = investment_summary
    
    print("\n--- 7. UK SPORT INVESTMENT BENCHMARK (RIO 2016 CYCLE) ---")
    print(f"  Pearson Correlation (Funding vs. Medals Won): {corr_rio:.3f}")
    print(f"  Mean Cost Per Medal: £{mean_cost_per_medal:.2f} Million")
    print(f"  Median Cost Per Medal: £{median_cost_per_medal:.2f} Million")
    print("\nMost Capital-Efficient Sports (Lowest £ per Medal):")
    print(pd.DataFrame(investment_summary["most_efficient_sports"]).to_string(index=False))
    print("\nCapital-Intensive Sports (Highest £ per Medal):")
    print(pd.DataFrame(investment_summary["least_efficient_funded_sports"]).to_string(index=False))

    # Save summary JSON
    with open(OUTPUT_STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[SUCCESS] Statistical audit saved to: {OUTPUT_STATS_PATH}")

if __name__ == "__main__":
    run_analysis()

