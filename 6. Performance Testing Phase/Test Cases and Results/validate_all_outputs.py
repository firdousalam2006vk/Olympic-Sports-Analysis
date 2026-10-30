"""
6. Performance Testing Phase/validate_all_outputs.py
Comprehensive 20-point quality assurance audit verifying all datasets,
statistical calculations, visualizations, and documentation files.

Author: Md. Firdous Alam
"""

import os
import sys
import pandas as pd
from PIL import Image

def find_root_dir():
    cur = os.path.abspath(__file__)
    for _ in range(5):
        cur = os.path.dirname(cur)
        if os.path.exists(os.path.join(cur, "5. Project Development Phase")):
            return cur
    return os.getcwd()

ROOT_DIR = find_root_dir()

def resolve_path(candidates):
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]

def run_system_validation():
    print("=" * 75)
    print("GLOBAL OLYMPIC PERFORMANCE ANALYSIS - SYSTEM AUDIT & QA MATRIX")
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

    # 1. Athletes Dataset
    ath_path = resolve_path([
        os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "athletes.csv"),
        os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "athletes.csv"),
        os.path.join(ROOT_DIR, "data", "athletes.csv")
    ])
    record_test("athletes.csv File Existence", os.path.exists(ath_path), f"Path: {ath_path}")
    
    ath_size = os.path.getsize(ath_path)
    ath_under_25mb = ath_size < (25 * 1024 * 1024)
    record_test("athletes.csv Strict Size < 25 MB (GitHub Upload Limit)", ath_under_25mb, f"Size: {ath_size:,} bytes ({ath_size/(1024*1024):.2f} MB)")
    
    df_ath = pd.read_csv(ath_path, low_memory=False)
    record_test("athletes.csv Modern Era (1980-2016) Row Count Check", len(df_ath) == 157417, f"Rows: {len(df_ath):,}")
    
    req_cols = ['athlete_id', 'name', 'sex', 'team', 'noc', 'country', 'continent', 'year', 'season', 'city', 'sport', 'event', 'medal', 'is_medalist']
    record_test("athletes.csv Schema Verification", all(c in df_ath.columns for c in req_cols), f"Columns: {len(df_ath.columns)}")
    
    null_core = df_ath[['athlete_id', 'name', 'sex', 'team', 'noc', 'year', 'season', 'sport', 'event']].isna().sum().sum()
    record_test("athletes.csv Core Attributes Non-Null Check", null_core == 0, f"Found {null_core} null values in core fields")
    
    valid_medals = set(df_ath['medal'].unique()) == {'No Medal', 'Gold', 'Silver', 'Bronze'}
    record_test("athletes.csv Standardized Medal Domain Check", valid_medals, f"Values: {df_ath['medal'].unique()}")

    # 2. Medal Results
    med_path = resolve_path([
        os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "medal_results.csv"),
        os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "medal_results.csv"),
        os.path.join(ROOT_DIR, "data", "medal_results.csv")
    ])
    record_test("medal_results.csv File Existence", os.path.exists(med_path), f"Path: {med_path}")
    
    df_med = pd.read_csv(med_path)
    record_test("medal_results.csv Row Count Check", len(df_med) == 3837, f"Rows: {len(df_med):,}")
    
    dups = df_med.duplicated(subset=['games_id', 'noc']).sum()
    record_test("medal_results.csv Composite PK Uniqueness ([games_id, noc])", dups == 0, f"Duplicate keys: {dups}")
    
    tot_mismatch = (df_med['gold'] + df_med['silver'] + df_med['bronze'] != df_med['total_medals']).sum()
    record_test("Mathematical Check: Total Medals = G + S + B", tot_mismatch == 0, f"Mismatches: {tot_mismatch}")
    
    weight_mismatch = (3*df_med['gold'] + 2*df_med['silver'] + 1*df_med['bronze'] != df_med['weighted_score']).sum()
    record_test("Mathematical Check: Weighted Score = 3G + 2S + 1B", weight_mismatch == 0, f"Mismatches: {weight_mismatch}")
    
    usa_row = df_med[df_med['noc'] == 'USA']
    usa_gold = usa_row['gold'].sum()
    usa_tot = usa_row['total_medals'].sum()
    record_test("Authentic USA Medal Tally Verification", (usa_gold == 1131) and (usa_tot == 2823), f"USA Gold: {usa_gold:,}, Total: {usa_tot:,}")

    # 3. Host Nation Performance
    host_path = resolve_path([
        os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "processed", "host_nation_performance.csv"),
        os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "processed", "host_nation_performance.csv")
    ])
    record_test("host_nation_performance.csv File Existence", os.path.exists(host_path), f"Path: {host_path}")
    
    df_host = pd.read_csv(host_path)
    valid_bumps = df_host['medal_bump'].dropna()
    surge_rate = (valid_bumps > 0).mean()
    mean_bump = valid_bumps.mean()
    record_test("Host Nation Surge Statistical Validity", (surge_rate >= 0.85) and (abs(mean_bump - 15.4) < 0.2), f"Surge rate: {surge_rate*100:.1f}%; Mean bump: +{mean_bump:.1f} medals")

    # 4. Regional Sports Efficiency
    reg_path = resolve_path([
        os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "processed", "regional_sports_efficiency.csv"),
        os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "processed", "regional_sports_efficiency.csv")
    ])
    record_test("regional_sports_efficiency.csv File Existence", os.path.exists(reg_path), f"Path: {reg_path}")
    
    df_reg = pd.read_csv(reg_path)
    record_test("Continental Partition Coverage Check", len(df_reg) >= 5, f"Continents: {sorted(df_reg['continent'].tolist())}")

    # 5. Funding Benchmark
    fund_path = resolve_path([
        os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "processed", "sports_funding_benchmark.csv"),
        os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "processed", "sports_funding_benchmark.csv")
    ])
    record_test("sports_funding_benchmark.csv File Existence", os.path.exists(fund_path), f"Path: {fund_path}")
    
    df_fund = pd.read_csv(fund_path)
    rio_fund = df_fund[df_fund['cycle'] == 'Rio 2016']
    corr = rio_fund['funding_millions_gbp'].corr(rio_fund['medals_won'])
    record_test("High-Performance Investment Correlation Check", abs(corr - 0.752) < 0.01, f"Pearson correlation r: {corr:.3f}")

    # 6. Visualizations
    charts = [
        "01_top_15_countries_medals.png",
        "02_gender_participation_trajectory.png",
        "03_host_nation_advantage.png",
        "04_regional_conversion_efficiency.png",
        "05_sports_funding_vs_medals_scatter.png"
    ]
    charts_ok = True
    for c in charts:
        c_path = resolve_path([
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Project Screenshots", c),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "charts", c)
        ])
        if not os.path.exists(c_path):
            charts_ok = False
            break
        img = Image.open(c_path)
        if img.size[0] < 2000:
            charts_ok = False
            break
    record_test("Exported 300 DPI Visualizations Check", charts_ok, f"Verified 5 charts with high-res dimensions")

    # 7. Core Documentation & 7-Phase PDFs
    docs = [
        resolve_path([os.path.join(ROOT_DIR, "1. Ideation Phase", "1_Ideation_Phase.pdf")]),
        resolve_path([os.path.join(ROOT_DIR, "2. Requirement Analysis", "2_Requirement_Analysis.pdf")]),
        resolve_path([os.path.join(ROOT_DIR, "3. Project Design Phase", "3_Project_Design.pdf")]),
        resolve_path([os.path.join(ROOT_DIR, "4. Project Planning Phase", "4_Project_Planning.pdf")]),
        resolve_path([os.path.join(ROOT_DIR, "5. Project Development Phase", "5_Project_Development.pdf")]),
        resolve_path([os.path.join(ROOT_DIR, "6. Performance Testing Phase", "6_Performance_Testing.pdf")]),
        resolve_path([os.path.join(ROOT_DIR, "7. Documentation and Demo", "7_Documentation_and_Demo.pdf")]),
        resolve_path([
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Final Project Report", "Project_Report.pdf"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "reports", "Project_Report.pdf")
        ]),
        resolve_path([
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Final Project Report", "Project_Presentation.pptx"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "presentation", "Project_Presentation.pptx")
        ]),
        resolve_path([
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Demo Video", "Olympic_Sports_Analysis_Demo_5_Minutes.mp4"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Demo Video", "Project_Demo.mp4"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "demo", "Project_Demo.mp4")
        ]),
        resolve_path([os.path.join(ROOT_DIR, "7. Documentation and Demo", "USER_GUIDE.md")]),
        resolve_path([os.path.join(ROOT_DIR, "README.md")]),
        resolve_path([os.path.join(ROOT_DIR, "requirements.txt")])
    ]
    docs_ok = all(os.path.exists(d) and os.path.getsize(d) > 100 for d in docs)
    record_test("All Project Documentation & 7-Phase PDFs Present", docs_ok, f"Verified 7 Phase PDFs + Core deliverables")

    print("-" * 75)
    print(f"AUDIT SUMMARY: {passed_tests} OF {total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 75)
    
    if passed_tests == total_tests:
        print("[SUCCESS] ALL DATASETS AND PROJECT ASSETS VERIFIED WITH 100% INTEGRITY.")
        return 0
    else:
        print(f"[FAIL] {total_tests - passed_tests} TEST(S) FAILED INTEGRITY VERIFICATION.")
        return 1

if __name__ == "__main__":
    sys.exit(run_system_validation())
