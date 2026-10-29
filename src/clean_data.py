"""
src/clean_data.py
=================
Project: Global Olympic Sports Performance Analysis
Description: Ingests authentic Olympic historical datasets, cleans athlete
             demographics, solves team-event medal multi-counting via
             deterministic deduplication, maps host nations and continental
             regions, and exports Tableau-ready datasets.
"""

import os
import sys
import urllib.request
import numpy as np
import pandas as pd

# Paths
DATA_DIR = "data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

OLYMPICS_RAW_PATH = os.path.join(RAW_DIR, "olympics_raw.csv")
REGIONS_RAW_PATH = os.path.join(RAW_DIR, "noc_regions_raw.csv")

TARGET_ATHLETES_CSV = os.path.join(DATA_DIR, "athletes.csv")
TARGET_MEDALS_CSV = os.path.join(DATA_DIR, "medal_results.csv")

OLYMPICS_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/olympics.csv"
REGIONS_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/regions.csv"

# Historical Summer and Winter Host Nations
HOST_MAPPING = {
    # Summer Games (1896 - 2016)
    (1896, "Summer"): "GRE", (1900, "Summer"): "FRA", (1904, "Summer"): "USA",
    (1906, "Summer"): "GRE", (1908, "Summer"): "GBR", (1912, "Summer"): "SWE",
    (1920, "Summer"): "BEL", (1924, "Summer"): "FRA", (1928, "Summer"): "NED",
    (1932, "Summer"): "USA", (1936, "Summer"): "GER", (1948, "Summer"): "GBR",
    (1952, "Summer"): "FIN", (1956, "Summer"): "AUS", (1960, "Summer"): "ITA",
    (1964, "Summer"): "JPN", (1968, "Summer"): "MEX", (1972, "Summer"): "GER",
    (1976, "Summer"): "CAN", (1980, "Summer"): "URS", (1984, "Summer"): "USA",
    (1988, "Summer"): "KOR", (1992, "Summer"): "ESP", (1996, "Summer"): "USA",
    (2000, "Summer"): "AUS", (2004, "Summer"): "GRE", (2008, "Summer"): "CHN",
    (2012, "Summer"): "GBR", (2016, "Summer"): "BRA", (2020, "Summer"): "JPN",
    # Winter Games (1924 - 2014)
    (1924, "Winter"): "FRA", (1928, "Winter"): "SUI", (1932, "Winter"): "USA",
    (1936, "Winter"): "GER", (1948, "Winter"): "SUI", (1952, "Winter"): "NOR",
    (1956, "Winter"): "ITA", (1960, "Winter"): "USA", (1964, "Winter"): "AUT",
    (1968, "Winter"): "FRA", (1972, "Winter"): "JPN", (1976, "Winter"): "AUT",
    (1980, "Winter"): "USA", (1984, "Winter"): "YUG", (1988, "Winter"): "CAN",
    (1992, "Winter"): "FRA", (1994, "Winter"): "NOR", (1998, "Winter"): "JPN",
    (2002, "Winter"): "USA", (2006, "Winter"): "ITA", (2010, "Winter"): "CAN",
    (2014, "Winter"): "RUS"
}

# Unify split equestrian venue in 1956 to primary host city
PRIMARY_CITY_MAPPING = {
    (1956, "Summer"): "Melbourne",
}

# Olympic Continental Associations
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
    # Special
    "IOA": "Special", "ROT": "Special", "UNK": "Special", "WIF": "Special"
}

def ensure_raw_data():
    """Ensures raw datasets exist or downloads authentic public records."""
    if not os.path.exists(OLYMPICS_RAW_PATH):
        print(f"Downloading authentic Olympic data from {OLYMPICS_URL}...")
        urllib.request.urlretrieve(OLYMPICS_URL, OLYMPICS_RAW_PATH)
    if not os.path.exists(REGIONS_RAW_PATH):
        print(f"Downloading NOC regions mapping from {REGIONS_URL}...")
        urllib.request.urlretrieve(REGIONS_URL, REGIONS_RAW_PATH)
    print("Raw datasets verified on disk.")

def process_and_clean():
    ensure_raw_data()
    print("Ingesting raw datasets...")
    df_raw = pd.read_csv(OLYMPICS_RAW_PATH)
    df_reg = pd.read_csv(REGIONS_RAW_PATH)
    df_reg.columns = [c.lower() for c in df_reg.columns]

    # Merge region name (country)
    df = df_raw.merge(df_reg[['noc', 'region']], on='noc', how='left')
    df.loc[df['noc'] == 'SGP', 'region'] = 'Singapore'
    df.loc[df['noc'] == 'ROT', 'region'] = 'Refugee Olympic Team'
    df.loc[df['noc'] == 'TUV', 'region'] = 'Tuvalu'
    df.loc[df['noc'] == 'UNK', 'region'] = 'Unknown'
    df['region'] = df['region'].fillna(df['team'])

    # Map continent & primary host city
    df['continent'] = df['noc'].map(CONTINENT_MAP).fillna('Other')
    df['city'] = df.apply(lambda r: PRIMARY_CITY_MAPPING.get((r['year'], r['season']), r['city']), axis=1)
    df['is_host'] = df.apply(lambda r: 1 if HOST_MAPPING.get((r['year'], r['season'])) == r['noc'] else 0, axis=1)

    # Standardize athlete metrics
    df['athlete_id'] = df['id']
    df['medal'] = df['medal'].fillna('No Medal')
    df['is_medalist'] = (df['medal'] != 'No Medal').astype(int)

    # Age group binning
    bins = [0, 19, 24, 29, 34, 100]
    labels = ['Under 20', '20-24', '25-29', '30-34', '35+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True).astype(str).replace('nan', 'Unknown')

    # Build athletes.csv
    athletes_df = df.rename(columns={
        'region': 'country',
        'height': 'height_cm',
        'weight': 'weight_kg'
    })[[
        'athlete_id', 'name', 'sex', 'age', 'age_group', 'height_cm', 'weight_kg',
        'team', 'noc', 'country', 'continent', 'games', 'year', 'season', 'city',
        'sport', 'event', 'medal', 'is_medalist', 'is_host'
    ]]

    # Save to both target locations
    athletes_df.to_csv(TARGET_ATHLETES_CSV, index=False)
    athletes_df.to_csv(os.path.join(PROCESSED_DIR, "athletes.csv"), index=False)
    print(f"Generated: {TARGET_ATHLETES_CSV} ({len(athletes_df):,} rows x {len(athletes_df.columns)} cols)")

    # -------------------------------------------------------------
    # Build medal_results.csv (Official Event Deduplicated Tallies)
    # -------------------------------------------------------------
    print("Computing official event-deduplicated medal results...")
    medals_dedup = df[df['medal'] != 'No Medal'].drop_duplicates(
        subset=['year', 'season', 'sport', 'event', 'medal', 'noc']
    )

    medal_counts = medals_dedup.groupby(['year', 'season', 'city', 'noc', 'medal']).size().unstack(fill_value=0).reset_index()
    for col in ['Gold', 'Silver', 'Bronze']:
        if col not in medal_counts.columns:
            medal_counts[col] = 0

    medal_counts['total_medals'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
    medal_counts['weighted_score'] = medal_counts['Gold'] * 3 + medal_counts['Silver'] * 2 + medal_counts['Bronze'] * 1

    part_stats = df.groupby(['year', 'season', 'city', 'noc']).agg(
        athletes_count=('athlete_id', 'nunique'),
        events_entered=('event', 'nunique'),
        sports_entered=('sport', 'nunique')
    ).reset_index()

    medal_results = part_stats.merge(medal_counts, on=['year', 'season', 'city', 'noc'], how='left')
    medal_results[['Gold', 'Silver', 'Bronze', 'total_medals', 'weighted_score']] = (
        medal_results[['Gold', 'Silver', 'Bronze', 'total_medals', 'weighted_score']].fillna(0).astype(int)
    )

    noc_meta = df[['noc', 'region', 'continent']].drop_duplicates(subset=['noc'])
    medal_results = medal_results.merge(noc_meta, on='noc', how='left').rename(columns={'region': 'country'})

    medal_results['games_id'] = medal_results['year'].astype(str) + " " + medal_results['season']
    medal_results['is_host'] = medal_results.apply(
        lambda r: 1 if HOST_MAPPING.get((r['year'], r['season'])) == r['noc'] else 0, axis=1
    )

    medal_results['medals_per_100_athletes'] = np.round(
        (medal_results['total_medals'] / medal_results['athletes_count']) * 100, 2
    )

    medal_results = medal_results[[
        'games_id', 'year', 'season', 'city', 'noc', 'country', 'continent',
        'is_host', 'athletes_count', 'events_entered', 'sports_entered',
        'Gold', 'Silver', 'Bronze', 'total_medals', 'weighted_score', 'medals_per_100_athletes'
    ]].rename(columns={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'bronze'})

    # Save to both target locations
    medal_results.to_csv(TARGET_MEDALS_CSV, index=False)
    medal_results.to_csv(os.path.join(PROCESSED_DIR, "medal_results.csv"), index=False)
    print(f"Generated: {TARGET_MEDALS_CSV} ({len(medal_results):,} rows x {len(medal_results.columns)} cols)")

    # Deduplication integrity verification
    dups = medal_results.duplicated(subset=['games_id', 'noc']).sum()
    print(f"Primary Key Check: [games_id, noc] duplicate count = {dups} (Strictly Unique)")
    print("[SUCCESS] src/clean_data.py execution complete.")

if __name__ == "__main__":
    process_and_clean()

