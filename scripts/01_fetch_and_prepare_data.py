"""
Script 01: Fetch and Prepare Authentic Olympic Data
===================================================
Project: Global Olympic Sports Performance Analysis
Author: Senior Data Analyst & Tableau Developer
Description: Downloads authentic historical Olympic dataset (1896-2016+)
             derived from IOC historical archives and sports-reference.
"""

import os
import sys
import urllib.request
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

OLYMPICS_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/olympics.csv"
REGIONS_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/regions.csv"

OLYMPICS_RAW_PATH = os.path.join(RAW_DIR, "olympics_raw.csv")
REGIONS_RAW_PATH = os.path.join(RAW_DIR, "noc_regions_raw.csv")

def download_file(url: str, dest_path: str):
    print(f"Downloading from {url} to {dest_path}...")
    def report_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = downloaded / total_size * 100
            if block_num % 1000 == 0 or downloaded >= total_size:
                print(f"  Progress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)", end="\r")
        else:
            if block_num % 1000 == 0:
                print(f"  Downloaded: {downloaded / (1024*1024):.1f} MB", end="\r")
    
    urllib.request.urlretrieve(url, dest_path, reporthook=report_progress)
    print(f"\nDownload complete: {dest_path} ({os.path.getsize(dest_path):,} bytes)")

def inspect_raw_data():
    print("\n--- Inspecting Downloaded Datasets ---")
    df_olympics = pd.read_csv(OLYMPICS_RAW_PATH)
    print(f"Olympics Raw Shape: {df_olympics.shape[0]:,} rows x {df_olympics.shape[1]} columns")
    print(f"Columns: {list(df_olympics.columns)}")
    print(f"Years covered: {df_olympics['year'].min()} to {df_olympics['year'].max()}")
    print(f"Seasons: {df_olympics['season'].unique()}")
    print(f"Unique Athletes: {df_olympics['id'].nunique():,}")
    print(f"Unique NOCs: {df_olympics['noc'].nunique():,}")
    
    df_regions = pd.read_csv(REGIONS_RAW_PATH)
    print(f"\nNOC Regions Raw Shape: {df_regions.shape[0]:,} rows x {df_regions.shape[1]} columns")
    print(f"Sample Regions:\n{df_regions.head(5)}")

if __name__ == "__main__":
    try:
        download_file(OLYMPICS_URL, OLYMPICS_RAW_PATH)
        download_file(REGIONS_URL, REGIONS_RAW_PATH)
        inspect_raw_data()
        print("\n[SUCCESS] Script 01 finished successfully.")
    except Exception as e:
        print(f"\n[ERROR] Failed to fetch data: {e}", file=sys.stderr)
        sys.exit(1)

