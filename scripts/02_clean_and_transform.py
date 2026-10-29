"""
Script 02: Clean, Standardize, and Transform Olympic Datasets
============================================================
Project: Global Olympic Sports Performance Analysis
Author: Senior Data Analyst & Tableau Developer
Description: Cleans raw Olympic data, deduplicates team event medals to match
             official IOC records, maps host countries, assigns Olympic continents,
             calculates efficiency metrics, and exports clean CSVs.
"""

import os
import sys
import numpy as np
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

OLYMPICS_RAW = os.path.join(RAW_DIR, "olympics_raw.csv")
REGIONS_RAW = os.path.join(RAW_DIR, "noc_regions_raw.csv")

# 1. Historical Host Country Mapping (Games -> Host NOC)
HOST_MAPPING = {
    # Summer
    (1896, "Summer"): "GRE",
    (1900, "Summer"): "FRA",
    (1904, "Summer"): "USA",
    (1906, "Summer"): "GRE",
    (1908, "Summer"): "GBR",
    (1912, "Summer"): "SWE",
    (1920, "Summer"): "BEL",
    (1924, "Summer"): "FRA",
    (1928, "Summer"): "NED",
    (1932, "Summer"): "USA",
    (1936, "Summer"): "GER",
    (1948, "Summer"): "GBR",
    (1952, "Summer"): "FIN",
    (1956, "Summer"): "AUS",  # Equestrian in SWE
    (1960, "Summer"): "ITA",
    (1964, "Summer"): "JPN",
    (1968, "Summer"): "MEX",
    (1972, "Summer"): "GER",
    (1976, "Summer"): "CAN",
    (1980, "Summer"): "URS",  # Soviet Union
    (1984, "Summer"): "USA",
    (1988, "Summer"): "KOR",
    (1992, "Summer"): "ESP",
    (1996, "Summer"): "USA",
    (2000, "Summer"): "AUS",
    (2004, "Summer"): "GRE",
    (2008, "Summer"): "CHN",
    (2012, "Summer"): "GBR",
    (2016, "Summer"): "BRA",
    (2020, "Summer"): "JPN",
    # Winter
    (1924, "Winter"): "FRA",
    (1928, "Winter"): "SUI",
    (1932, "Winter"): "USA",
    (1936, "Winter"): "GER",
    (1948, "Winter"): "SUI",
    (1952, "Winter"): "NOR",
    (1956, "Winter"): "ITA",
    (1960, "Winter"): "USA",
    (1964, "Winter"): "AUT",
    (1968, "Winter"): "FRA",
    (1972, "Winter"): "JPN",
    (1976, "Winter"): "AUT",
    (1980, "Winter"): "USA",
    (1984, "Winter"): "YUG",
    (1988, "Winter"): "CAN",
    (1992, "Winter"): "FRA",
    (1994, "Winter"): "NOR",
    (1998, "Winter"): "JPN",
    (2002, "Winter"): "USA",
    (2006, "Winter"): "ITA",
    (2010, "Winter"): "CAN",
    (2014, "Winter"): "RUS"
}

# Primary host city mapping (unifies split locations like 1956 Melbourne/Stockholm)
PRIMARY_CITY_MAPPING = {
    (1956, "Summer"): "Melbourne",
}

# 2. Continent Mapping based on Olympic Continental Associations
CONTINENT_MAP = {
    # Americas
    "USA": "Americas", "CAN": "Americas", "MEX": "Americas", "CUB": "Americas",
    "BRA": "Americas", "ARG": "Americas", "JAM": "Americas", "COL": "Americas",
    "CHI": "Americas", "VEN": "Americas", "PER": "Americas", "URU": "Americas",
    "PUR": "Americas", "TRI": "Americas", "ECU": "Americas", "DOM": "Americas",
    "BAH": "Americas", "PAN": "Americas", "CRC": "Americas", "GUA": "Americas",
    "SUR": "Americas", "GUY": "Americas", "BAR": "Americas", "BER": "Americas",
    "HAI": "Americas", "ISV": "Americas", "AHO": "Americas", "ANT": "Americas",
    "ARU": "Americas", "BIZ": "Americas", "BOL": "Americas", "CAY": "Americas",
    "DMA": "Americas", "ESA": "Americas", "GRN": "Americas", "HON": "Americas",
    "IVB": "Americas", "NCA": "Americas", "PAR": "Americas", "SKN": "Americas",
    "LCA": "Americas", "VIN": "Americas",
    
    # Europe
    "GBR": "Europe", "FRA": "Europe", "GER": "Europe", "ITA": "Europe",
    "RUS": "Europe", "URS": "Europe", "GDR": "Europe", "FRG": "Europe",
    "EUN": "Europe", "SWE": "Europe", "NOR": "Europe", "FIN": "Europe",
    "NED": "Europe", "HUN": "Europe", "ESP": "Europe", "BEL": "Europe",
    "POL": "Europe", "SUI": "Europe", "AUT": "Europe", "ROU": "Europe",
    "TCH": "Europe", "CZE": "Europe", "YUG": "Europe", "GRE": "Europe",
    "DEN": "Europe", "UKR": "Europe", "BUL": "Europe", "BLR": "Europe",
    "TUR": "Europe", "IRL": "Europe", "CRO": "Europe", "SCG": "Europe",
    "SVK": "Europe", "EST": "Europe", "LAT": "Europe", "LTU": "Europe",
    "POR": "Europe", "SLO": "Europe", "GEO": "Europe", "ARM": "Europe",
    "AZE": "Europe", "MDA": "Europe", "CYP": "Europe", "ISL": "Europe",
    "LUX": "Europe", "ISR": "Europe", "ALB": "Europe", "AND": "Europe",
    "BIH": "Europe", "KOS": "Europe", "LIE": "Europe", "MLT": "Europe",
    "MNE": "Europe", "MON": "Europe", "MKD": "Europe", "SMR": "Europe",
    
    # Asia
    "CHN": "Asia", "JPN": "Asia", "KOR": "Asia", "IND": "Asia", "IRI": "Asia",
    "KAZ": "Asia", "PRK": "Asia", "TPE": "Asia", "THA": "Asia", "UZB": "Asia",
    "INA": "Asia", "PHI": "Asia", "MGL": "Asia", "MAS": "Asia", "PAK": "Asia",
    "SGP": "Asia", "HKG": "Asia", "VIE": "Asia", "QAT": "Asia", "BRN": "Asia",
    "KUW": "Asia", "KSA": "Asia", "UAE": "Asia", "SYR": "Asia", "JOR": "Asia",
    "LIB": "Asia", "AFG": "Asia", "IRQ": "Asia", "SRI": "Asia", "KGZ": "Asia",
    "TJK": "Asia", "TKM": "Asia", "BAN": "Asia", "BHU": "Asia", "BRU": "Asia",
    "CAM": "Asia", "LAO": "Asia", "MDV": "Asia", "MYA": "Asia", "NEP": "Asia",
    "OMA": "Asia", "PLE": "Asia", "TLS": "Asia", "YEM": "Asia",
    
    # Africa
    "KEN": "Africa", "ETH": "Africa", "RSA": "Africa", "EGY": "Africa",
    "NGR": "Africa", "MAR": "Africa", "ALG": "Africa", "TUN": "Africa",
    "UGA": "Africa", "CMR": "Africa", "ZIM": "Africa", "GHA": "Africa",
    "CIV": "Africa", "SEN": "Africa", "ZAM": "Africa", "BOT": "Africa",
    "NAM": "Africa", "MOZ": "Africa", "BUR": "Africa", "TAN": "Africa",
    "ERI": "Africa", "GAB": "Africa", "SUD": "Africa", "TOG": "Africa",
    "ANG": "Africa", "BEN": "Africa", "CAF": "Africa", "CHA": "Africa",
    "COM": "Africa", "CGO": "Africa", "COD": "Africa", "DJI": "Africa",
    "GEQ": "Africa", "GAM": "Africa", "GUI": "Africa", "GBS": "Africa",
    "LBA": "Africa", "LES": "Africa", "LBR": "Africa", "MAD": "Africa",
    "MAW": "Africa", "MLI": "Africa", "MTN": "Africa", "MRI": "Africa",
    "NIG": "Africa", "RWA": "Africa", "STP": "Africa", "SEY": "Africa",
    "SLE": "Africa", "SOM": "Africa", "SSD": "Africa", "SWZ": "Africa",
    
    # Oceania
    "AUS": "Oceania", "NZL": "Oceania", "FIJ": "Oceania", "SAM": "Oceania",
    "TGA": "Oceania", "PNG": "Oceania", "ASA": "Oceania", "COK": "Oceania",
    "FSM": "Oceania", "GUM": "Oceania", "KIR": "Oceania", "MHL": "Oceania",
    "NRU": "Oceania", "PLW": "Oceania", "SOL": "Oceania", "TUV": "Oceania",
    "VAN": "Oceania", "ANZ": "Oceania",
    
    # Special / Independent
    "IOA": "Special", "ROT": "Special", "UNK": "Special", "WIF": "Special"
}

def clean_data():
    print("Loading raw files...")
    df_raw = pd.read_csv(OLYMPICS_RAW)
    df_reg = pd.read_csv(REGIONS_RAW)
    
    # Standardize column names
    df_reg.columns = [c.lower() for c in df_reg.columns]
    
    # Merge region (country name)
    df = df_raw.merge(df_reg[['noc', 'region']], on='noc', how='left')
    
    # Fill missing country names cleanly
    df.loc[df['noc'] == 'SGP', 'region'] = 'Singapore'
    df.loc[df['noc'] == 'ROT', 'region'] = 'Refugee Olympic Team'
    df.loc[df['noc'] == 'TUV', 'region'] = 'Tuvalu'
    df.loc[df['noc'] == 'UNK', 'region'] = 'Unknown'
    df['region'] = df['region'].fillna(df['team'])
    
    # Map continents
    df['continent'] = df['noc'].map(CONTINENT_MAP).fillna('Other')
    
    # Standardize primary host city (e.g. Melbourne in 1956)
    df['city'] = df.apply(lambda r: PRIMARY_CITY_MAPPING.get((r['year'], r['season']), r['city']), axis=1)
    
    # Map Host status
    df['is_host'] = df.apply(lambda r: 1 if HOST_MAPPING.get((r['year'], r['season'])) == r['noc'] else 0, axis=1)
    
    # Add athlete_id alias to df
    df['athlete_id'] = df['id']
    
    # Clean medal column
    df['has_medal'] = df['medal'].notna().astype(int)
    df['medal'] = df['medal'].fillna('No Medal')
    df['is_medalist'] = (df['medal'] != 'No Medal').astype(int)
    
    # Age group binning
    bins = [0, 19, 24, 29, 34, 100]
    labels = ['Under 20', '20-24', '25-29', '30-34', '35+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True).astype(str).replace('nan', 'Unknown')
    
    # Standardized athlete dataset
    athletes_df = df.rename(columns={
        'region': 'country',
        'height': 'height_cm',
        'weight': 'weight_kg'
    })[[
        'athlete_id', 'name', 'sex', 'age', 'age_group', 'height_cm', 'weight_kg',
        'team', 'noc', 'country', 'continent', 'games', 'year', 'season', 'city',
        'sport', 'event', 'medal', 'is_medalist', 'is_host'
    ]]
    
    athletes_path = os.path.join(PROCESSED_DIR, "athletes.csv")
    athletes_df.to_csv(athletes_path, index=False)
    print(f"Saved: {athletes_path} ({athletes_df.shape[0]:,} rows x {athletes_df.shape[1]} cols)")
    
    # -------------------------------------------------------------
    # 2. Build medal_results.csv (Official Event Deduplicated Tallies)
    # -------------------------------------------------------------
    print("\nComputing official deduplicated medal results...")
    
    # Subset of medalists, deduplicated by event & medal & country
    medals_dedup = df[df['medal'] != 'No Medal'].drop_duplicates(
        subset=['year', 'season', 'sport', 'event', 'medal', 'noc']
    )
    
    # Pivot medal types
    medal_counts = medals_dedup.groupby(['year', 'season', 'city', 'noc', 'medal']).size().unstack(fill_value=0).reset_index()
    for col in ['Gold', 'Silver', 'Bronze']:
        if col not in medal_counts.columns:
            medal_counts[col] = 0
            
    medal_counts['total_medals'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
    medal_counts['weighted_score'] = medal_counts['Gold'] * 3 + medal_counts['Silver'] * 2 + medal_counts['Bronze'] * 1
    
    # Participation metrics per Games & Country
    part_stats = df.groupby(['year', 'season', 'city', 'noc']).agg(
        athletes_count=('athlete_id', 'nunique'),
        events_entered=('event', 'nunique'),
        sports_entered=('sport', 'nunique')
    ).reset_index()
    
    # Merge participation with medal counts
    medal_results = part_stats.merge(medal_counts, on=['year', 'season', 'city', 'noc'], how='left')
    medal_results[['Gold', 'Silver', 'Bronze', 'total_medals', 'weighted_score']] = (
        medal_results[['Gold', 'Silver', 'Bronze', 'total_medals', 'weighted_score']].fillna(0).astype(int)
    )
    
    # Add country, continent, host metadata
    noc_meta = df[['noc', 'region', 'continent']].drop_duplicates(subset=['noc'])
    medal_results = medal_results.merge(noc_meta, on='noc', how='left').rename(columns={'region': 'country'})
    
    medal_results['games_id'] = medal_results['year'].astype(str) + " " + medal_results['season']
    medal_results['is_host'] = medal_results.apply(
        lambda r: 1 if HOST_MAPPING.get((r['year'], r['season'])) == r['noc'] else 0, axis=1
    )
    
    # Conversion Efficiency (Medals per 100 Athletes)
    medal_results['medals_per_100_athletes'] = np.round(
        (medal_results['total_medals'] / medal_results['athletes_count']) * 100, 2
    )
    
    # Reorder columns cleanly
    medal_results = medal_results[[
        'games_id', 'year', 'season', 'city', 'noc', 'country', 'continent',
        'is_host', 'athletes_count', 'events_entered', 'sports_entered',
        'Gold', 'Silver', 'Bronze', 'total_medals', 'weighted_score', 'medals_per_100_athletes'
    ]].rename(columns={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'bronze'})
    
    medal_results_path = os.path.join(PROCESSED_DIR, "medal_results.csv")
    medal_results.to_csv(medal_results_path, index=False)
    print(f"Saved: {medal_results_path} ({medal_results.shape[0]:,} rows x {medal_results.shape[1]} cols)")
    
    # -------------------------------------------------------------
    # 3. Build host_nation_performance.csv (Host Bump Analysis)
    # -------------------------------------------------------------
    print("\nComputing Host Nation Advantage Metrics (Pre, Host, Post)...")
    host_records = []
    
    summer_hosts = [
        (1952, "FIN", "Finland", "Helsinki"),
        (1956, "AUS", "Australia", "Melbourne"),
        (1960, "ITA", "Italy", "Rome"),
        (1964, "JPN", "Japan", "Tokyo"),
        (1968, "MEX", "Mexico", "Mexico City"),
        (1972, "GER", "Germany", "Munich"),
        (1976, "CAN", "Canada", "Montreal"),
        (1980, "URS", "Soviet Union", "Moscow"),
        (1984, "USA", "United States", "Los Angeles"),
        (1988, "KOR", "South Korea", "Seoul"),
        (1992, "ESP", "Spain", "Barcelona"),
        (1996, "USA", "United States", "Atlanta"),
        (2000, "AUS", "Australia", "Sydney"),
        (2004, "GRE", "Greece", "Athens"),
        (2008, "CHN", "China", "Beijing"),
        (2012, "GBR", "Great Britain", "London"),
        (2016, "BRA", "Brazil", "Rio de Janeiro")
    ]
    
    def get_stats(noc, year, season="Summer"):
        match = medal_results[(medal_results['noc'] == noc) & (medal_results['year'] == year) & (medal_results['season'] == season)]
        if len(match) > 0:
            row = match.iloc[0]
            return row['total_medals'], row['gold'], row['athletes_count']
        return np.nan, np.nan, np.nan

    summer_years = sorted(medal_results[medal_results['season'] == 'Summer']['year'].unique())

    for year, noc, country, city in summer_hosts:
        idx = summer_years.index(year)
        prev_year = summer_years[idx-1] if idx > 0 else None
        next_year = summer_years[idx+1] if idx < len(summer_years) - 1 else None
        
        host_medals, host_gold, host_athletes = get_stats(noc, year)
        pre_medals, pre_gold, pre_athletes = get_stats(noc, prev_year) if prev_year else (np.nan, np.nan, np.nan)
        post_medals, post_gold, post_athletes = get_stats(noc, next_year) if next_year else (np.nan, np.nan, np.nan)
        
        bump = host_medals - pre_medals if pd.notna(host_medals) and pd.notna(pre_medals) else np.nan
        bump_pct = (bump / pre_medals * 100) if pd.notna(bump) and pre_medals > 0 else np.nan
        
        host_records.append({
            'host_year': year,
            'host_city': city,
            'noc': noc,
            'country': country,
            'pre_games_year': prev_year,
            'pre_medals': pre_medals,
            'pre_gold': pre_gold,
            'pre_athletes': pre_athletes,
            'host_medals': host_medals,
            'host_gold': host_gold,
            'host_athletes': host_athletes,
            'post_games_year': next_year,
            'post_medals': post_medals,
            'post_gold': post_gold,
            'post_athletes': post_athletes,
            'medal_bump': bump,
            'medal_bump_pct': np.round(bump_pct, 1) if pd.notna(bump_pct) else np.nan
        })
        
    host_df = pd.DataFrame(host_records)
    host_path = os.path.join(PROCESSED_DIR, "host_nation_performance.csv")
    host_df.to_csv(host_path, index=False)
    print(f"Saved: {host_path} ({host_df.shape[0]} rows x {host_df.shape[1]} cols)")
    
    # -------------------------------------------------------------
    # 4. Build regional_sports_efficiency.csv (Continental Benchmarks)
    # -------------------------------------------------------------
    print("\nComputing Regional Sports Efficiency Benchmarks...")
    reg_summary = medal_results.groupby('continent').agg(
        total_editions=('games_id', 'nunique'),
        participating_nocs=('noc', 'nunique'),
        total_athlete_participations=('athletes_count', 'sum'),
        total_gold=('gold', 'sum'),
        total_silver=('silver', 'sum'),
        total_bronze=('bronze', 'sum'),
        total_medals=('total_medals', 'sum'),
        total_weighted_score=('weighted_score', 'sum')
    ).reset_index()
    
    reg_summary['medals_per_100_athletes'] = np.round(
        (reg_summary['total_medals'] / reg_summary['total_athlete_participations']) * 100, 2
    )
    reg_summary['gold_share_pct'] = np.round(
        (reg_summary['total_gold'] / reg_summary['total_medals']) * 100, 2
    )
    
    reg_path = os.path.join(PROCESSED_DIR, "regional_sports_efficiency.csv")
    reg_summary.to_csv(reg_path, index=False)
    print(f"Saved: {reg_path} ({reg_summary.shape[0]} rows x {reg_summary.shape[1]} cols)")

    # -------------------------------------------------------------
    # 5. Build sports_funding_benchmark.csv (Verified High-Perf Investment)
    # -------------------------------------------------------------
    print("\nBuilding sports_funding_benchmark.csv (UK Sport Official Olympic Cycle Grants)...")
    funding_data = [
        # Rio 2016 Cycle (2013-2017)
        {"sport": "Rowing", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 32.62, "medals_won": 5, "target_met": "Yes"},
        {"sport": "Cycling", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 30.27, "medals_won": 12, "target_met": "Yes"},
        {"sport": "Athletics", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 26.82, "medals_won": 7, "target_met": "Yes"},
        {"sport": "Sailing", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 25.50, "medals_won": 3, "target_met": "Yes"},
        {"sport": "Swimming", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 20.79, "medals_won": 6, "target_met": "Yes"},
        {"sport": "Canoeing", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 20.04, "medals_won": 4, "target_met": "Yes"},
        {"sport": "Equestrian", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 17.99, "medals_won": 3, "target_met": "Yes"},
        {"sport": "Gymnastics", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 14.61, "medals_won": 7, "target_met": "Yes"},
        {"sport": "Boxing", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 13.76, "medals_won": 3, "target_met": "Yes"},
        {"sport": "Hockey", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 16.11, "medals_won": 1, "target_met": "Yes"},
        {"sport": "Taekwondo", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 8.05, "medals_won": 3, "target_met": "Yes"},
        {"sport": "Diving", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 7.47, "medals_won": 3, "target_met": "Yes"},
        {"sport": "Judo", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 7.37, "medals_won": 1, "target_met": "Yes"},
        {"sport": "Triathlon", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 5.50, "medals_won": 3, "target_met": "Yes"},
        {"sport": "Shooting", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 3.95, "medals_won": 2, "target_met": "Yes"},
        {"sport": "Badminton", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 5.74, "medals_won": 1, "target_met": "Yes"},
        {"sport": "Modern Pentathlon", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 6.97, "medals_won": 0, "target_met": "No"},
        {"sport": "Fencing", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 4.23, "medals_won": 0, "target_met": "No"},
        {"sport": "Archery", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 2.95, "medals_won": 0, "target_met": "No"},
        {"sport": "Weightlifting", "cycle": "Rio 2016", "games_year": 2016, "funding_millions_gbp": 1.71, "medals_won": 0, "target_met": "No"},
        
        # London 2012 Cycle (2009-2013)
        {"sport": "Rowing", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 27.29, "medals_won": 9, "target_met": "Yes"},
        {"sport": "Cycling", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 26.03, "medals_won": 12, "target_met": "Yes"},
        {"sport": "Athletics", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 25.15, "medals_won": 6, "target_met": "Yes"},
        {"sport": "Swimming", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 25.14, "medals_won": 3, "target_met": "No"},
        {"sport": "Sailing", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 22.94, "medals_won": 5, "target_met": "Yes"},
        {"sport": "Canoeing", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 16.32, "medals_won": 4, "target_met": "Yes"},
        {"sport": "Hockey", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 15.01, "medals_won": 1, "target_met": "Yes"},
        {"sport": "Equestrian", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 13.39, "medals_won": 5, "target_met": "Yes"},
        {"sport": "Gymnastics", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 10.77, "medals_won": 4, "target_met": "Yes"},
        {"sport": "Boxing", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 9.50, "medals_won": 5, "target_met": "Yes"},
        {"sport": "Diving", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 7.73, "medals_won": 1, "target_met": "Yes"},
        {"sport": "Judo", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 7.49, "medals_won": 2, "target_met": "Yes"},
        {"sport": "Modern Pentathlon", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 6.29, "medals_won": 1, "target_met": "Yes"},
        {"sport": "Triathlon", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 5.29, "medals_won": 2, "target_met": "Yes"},
        {"sport": "Taekwondo", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 4.83, "medals_won": 2, "target_met": "Yes"},
        {"sport": "Shooting", "cycle": "London 2012", "games_year": 2012, "funding_millions_gbp": 2.46, "medals_won": 1, "target_met": "Yes"}
    ]
    df_funding = pd.DataFrame(funding_data)
    df_funding['cost_per_medal_millions_gbp'] = np.where(
        df_funding['medals_won'] > 0,
        np.round(df_funding['funding_millions_gbp'] / df_funding['medals_won'], 2),
        np.nan
    )
    df_funding['data_source'] = "UK Sport Official Published High Performance Grants"
    
    funding_path = os.path.join(PROCESSED_DIR, "sports_funding_benchmark.csv")
    df_funding.to_csv(funding_path, index=False)
    print(f"Saved: {funding_path} ({df_funding.shape[0]} rows x {df_funding.shape[1]} cols)")

if __name__ == "__main__":
    clean_data()
    print("\n[SUCCESS] Script 02 finished successfully.")
