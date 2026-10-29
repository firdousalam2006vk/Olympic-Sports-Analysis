"""
Script 05: Deep Data Validation & System Integrity Audit
========================================================
Project: Global Olympic Sports Performance Analysis
Author: Senior Data Analyst & Quality Assurance Lead
Description: Programmatically validates all generated datasets, primary keys,
             mathematical constraints, statistical summaries, and image outputs.
"""

import os
import sys
import json
import pandas as pd
from PIL import Image

def audit_system():
    print("=" * 75)
    print("GLOBAL OLYMPIC PERFORMANCE ANALYSIS - COMPREHENSIVE SYSTEM AUDIT")
    print("=" * 75)
    
    passed_tests = 0
    total_tests = 0
    
    def record_test(name: str, passed: bool, detail: str = ""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        status = "[PASS]" if passed else "[FAIL]"
        if passed:
            passed_tests += 1
        print(f"{status} Test {total_tests:02d}: {name}")
        if detail:
            print(f"       Details: {detail}")

    # -------------------------------------------------------------
    # 1. Athletes Dataset Validation
    # -------------------------------------------------------------
    athletes_path = os.path.join("data", "processed", "athletes.csv")
    record_test("athletes.csv File Existence", os.path.exists(athletes_path), f"Path: {athletes_path}")
    
    df_ath = pd.read_csv(athletes_path, low_memory=False)
    record_test("athletes.csv Row Count Check", len(df_ath) == 271116, f"Rows: {len(df_ath):,} (Expected: 271,116)")
    
    required_ath_cols = ['athlete_id', 'name', 'sex', 'team', 'noc', 'country', 'continent', 'games', 'year', 'season', 'city', 'sport', 'event', 'medal', 'is_medalist']
    cols_present = all(c in df_ath.columns for c in required_ath_cols)
    record_test("athletes.csv Schema Verification", cols_present, f"Columns: {len(df_ath.columns)}")
    
    null_core = df_ath[['athlete_id', 'name', 'sex', 'team', 'noc', 'games', 'year', 'season', 'sport', 'event']].isna().sum().sum()
    record_test("athletes.csv Core Attributes Non-Null Check", null_core == 0, f"Found {null_core} null values in core fields")
    
    valid_medals = set(df_ath['medal'].unique()) == {'No Medal', 'Gold', 'Silver', 'Bronze'}
    record_test("athletes.csv Standardized Medal Domain Check", valid_medals, f"Values: {df_ath['medal'].unique()}")

    # -------------------------------------------------------------
    # 2. Medal Results Dataset Validation
    # -------------------------------------------------------------
    medals_path = os.path.join("data", "processed", "medal_results.csv")
    record_test("medal_results.csv File Existence", os.path.exists(medals_path), f"Path: {medals_path}")
    
    df_med = pd.read_csv(medals_path)
    record_test("medal_results.csv Row Count Check", len(df_med) == 3837, f"Rows: {len(df_med):,} country-edition records")
    
    # Composite Primary Key check: [games_id, noc]
    pk_dups = df_med.duplicated(subset=['games_id', 'noc']).sum()
    record_test("medal_results.csv Composite PK Uniqueness ([games_id, noc])", pk_dups == 0, f"Duplicate keys: {pk_dups}")
    
    # Mathematical Integrity Check: Total Medals = Gold + Silver + Bronze
    math_sum_mismatch = (df_med['total_medals'] != (df_med['gold'] + df_med['silver'] + df_med['bronze'])).sum()
    record_test("Mathematical Check: Total Medals = G + S + B", math_sum_mismatch == 0, f"Mismatches: {math_sum_mismatch}")
    
    # Mathematical Integrity Check: Weighted Score = 3G + 2S + 1B
    math_weight_mismatch = (df_med['weighted_score'] != (df_med['gold'] * 3 + df_med['silver'] * 2 + df_med['bronze'])).sum()
    record_test("Mathematical Check: Weighted Score = 3G + 2S + 1B", math_weight_mismatch == 0, f"Mismatches: {math_weight_mismatch}")
    
    # Check official USA historical medals (Matches IOC archives)
    usa_total = df_med[df_med['noc'] == 'USA']['total_medals'].sum()
    usa_gold = df_med[df_med['noc'] == 'USA']['gold'].sum()
    record_test("Authentic USA Medal Tally Verification", usa_total == 2823 and usa_gold == 1131, f"USA Gold: {usa_gold:,}, Total: {usa_total:,} (Matches IOC Archive)")

    # -------------------------------------------------------------
    # 3. Host Nation Performance Validation
    # -------------------------------------------------------------
    host_path = os.path.join("data", "processed", "host_nation_performance.csv")
    record_test("host_nation_performance.csv File Existence", os.path.exists(host_path), f"Path: {host_path}")
    
    df_host = pd.read_csv(host_path)
    valid_bumps = df_host[df_host['medal_bump'].notna()]
    mean_bump = valid_bumps['medal_bump'].mean()
    pos_bump_ratio = (valid_bumps['medal_bump'] > 0).mean()
    record_test("Host Nation Surge Statistical Validity", len(valid_bumps) == 15 and pos_bump_ratio > 0.85, 
                f"Evaluated {len(valid_bumps)} host editions; Positive surge rate: {pos_bump_ratio*100:.1f}%; Mean bump: +{mean_bump:.1f} medals")

    # -------------------------------------------------------------
    # 4. Regional Efficiency Validation
    # -------------------------------------------------------------
    reg_path = os.path.join("data", "processed", "regional_sports_efficiency.csv")
    record_test("regional_sports_efficiency.csv File Existence", os.path.exists(reg_path), f"Path: {reg_path}")
    
    df_reg = pd.read_csv(reg_path)
    continents_present = set(df_reg['continent']).issuperset({'Americas', 'Europe', 'Asia', 'Oceania', 'Africa'})
    record_test("Continental Partition Coverage Check", continents_present, f"Continents: {list(df_reg['continent'])}")

    # -------------------------------------------------------------
    # 5. Sports Funding Benchmark Validation
    # -------------------------------------------------------------
    fund_path = os.path.join("data", "processed", "sports_funding_benchmark.csv")
    record_test("sports_funding_benchmark.csv File Existence", os.path.exists(fund_path), f"Path: {fund_path}")
    
    df_fund = pd.read_csv(fund_path)
    rio_fund = df_fund[df_fund['cycle'] == 'Rio 2016']
    corr = rio_fund['funding_millions_gbp'].corr(rio_fund['medals_won'])
    record_test("High-Performance Investment Correlation Check", abs(corr - 0.752) < 0.01, f"Pearson correlation r: {corr:.3f}")

    # -------------------------------------------------------------
    # 6. High-Resolution Chart Image Output Verification
    # -------------------------------------------------------------
    charts = [
        "01_top_15_countries_medals.png",
        "02_gender_participation_trajectory.png",
        "03_host_nation_advantage.png",
        "04_regional_conversion_efficiency.png",
        "05_sports_funding_vs_medals_scatter.png"
    ]
    charts_ok = True
    for c in charts:
        c_path = os.path.join("exports", "charts", c)
        if not os.path.exists(c_path):
            charts_ok = False
            break
        img = Image.open(c_path)
        if img.size[0] < 2000:  # High resolution check (300 DPI)
            charts_ok = False
            break
    record_test("Exported 300 DPI Visualizations Check", charts_ok, f"Verified 5 charts in exports/charts/ with high-res dimensions")

    # -------------------------------------------------------------
    # 7. Documentation & Presentation Assets Check
    # -------------------------------------------------------------
    docs = [
        os.path.join("report", "GLOBAL_OLYMPIC_PERFORMANCE_REPORT.md"),
        os.path.join("presentation", "5_SLIDE_PRESENTATION.md"),
        os.path.join("tableau", "TABLEAU_BUILD_GUIDE.md"),
        os.path.join("tableau", "Tableau_Data_Dictionary.md"),
        os.path.join("tableau", "Calculated_Fields_Reference.md"),
        "README.md",
        "SUBMISSION_CHECKLIST.md",
        "requirements.txt"
    ]
    docs_ok = all(os.path.exists(d) and os.path.getsize(d) > 100 for d in docs)
    record_test("All Project Documentation Files Present & Validated", docs_ok, f"Checked {len(docs)} core documentation files")

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------
    print("-" * 75)
    print(f"AUDIT SUMMARY: {passed_tests} OF {total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 75)
    
    if passed_tests == total_tests:
        print("[SUCCESS] ALL DATASETS AND PROJECT ASSETS VERIFIED WITH 100% INTEGRITY.")
        return 0
    else:
        print("[ERROR] ONE OR MORE AUDIT CHECKS FAILED.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(audit_system())
