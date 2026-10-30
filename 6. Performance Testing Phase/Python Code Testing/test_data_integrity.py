"""
6. Performance Testing Phase/test_data_integrity.py
Automated 10-point unit test suite verifying schema definitions,
file sizes, arithmetic calculations, and deduplication accuracy.

Author: Md. Firdous Alam
"""

import os
import unittest
import pandas as pd

def find_root_dir():
    cur = os.path.abspath(__file__)
    for _ in range(5):
        cur = os.path.dirname(cur)
        if os.path.exists(os.path.join(cur, "5. Project Development Phase")):
            return cur
    return os.getcwd()

ROOT_DIR = find_root_dir()

def resolve_file(candidates):
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]

class TestOlympicDataIntegrity(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.athletes_path = resolve_file([
            os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "athletes.csv"),
            os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "athletes.csv"),
            os.path.join(ROOT_DIR, "data", "athletes.csv")
        ])
        cls.medals_path = resolve_file([
            os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "medal_results.csv"),
            os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "medal_results.csv"),
            os.path.join(ROOT_DIR, "data", "medal_results.csv")
        ])
        cls.host_path = resolve_file([
            os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "processed", "host_nation_performance.csv"),
            os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "processed", "host_nation_performance.csv")
        ])
        cls.efficiency_path = resolve_file([
            os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "processed", "regional_sports_efficiency.csv"),
            os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "processed", "regional_sports_efficiency.csv")
        ])
        cls.funding_path = resolve_file([
            os.path.join(ROOT_DIR, "5. Project Development Phase", "Dataset Collection", "processed", "sports_funding_benchmark.csv"),
            os.path.join(ROOT_DIR, "5. Project Development Phase", "data", "processed", "sports_funding_benchmark.csv")
        ])
        
        cls.df_athletes = pd.read_csv(cls.athletes_path, low_memory=False)
        cls.df_medals = pd.read_csv(cls.medals_path)

    def test_01_athletes_file_size_below_25mb(self):
        """Verify athletes.csv strictly respects GitHub's 25 MB web upload limit."""
        size_bytes = os.path.getsize(self.athletes_path)
        limit_bytes = 25 * 1024 * 1024
        self.assertLess(size_bytes, limit_bytes, f"athletes.csv exceeds 25 MB: {size_bytes} bytes")

    def test_02_athletes_schema_and_rows(self):
        """Verify modern era athletes dataset contains 157,417 rows and 18 columns."""
        self.assertEqual(len(self.df_athletes), 157417, "athletes.csv row count mismatch")
        self.assertEqual(len(self.df_athletes.columns), 18, "athletes.csv column count mismatch")
        expected_cols = ['athlete_id', 'name', 'sex', 'age', 'height_cm', 'weight_kg', 'team',
                         'noc', 'country', 'continent', 'year', 'season', 'city', 'sport',
                         'event', 'medal', 'is_medalist', 'is_host']
        for col in expected_cols:
            self.assertIn(col, self.df_athletes.columns, f"Missing required column: {col}")

    def test_03_medal_results_uniqueness(self):
        """Verify medal_results.csv has zero duplicate primary keys across [games_id, noc]."""
        year_col = "games_id" if "games_id" in self.df_medals.columns else "Year"
        noc_col = "noc" if "noc" in self.df_medals.columns else "NOC"
        dups = self.df_medals.duplicated(subset=[year_col, noc_col]).sum()
        self.assertEqual(dups, 0, f"Found {dups} duplicate primary keys in medal_results.csv")

    def test_04_medal_arithmetic_consistency(self):
        """Verify Total_Medals = Gold + Silver + Bronze for all country-edition records."""
        g_col = "gold" if "gold" in self.df_medals.columns else "Gold"
        s_col = "silver" if "silver" in self.df_medals.columns else "Silver"
        b_col = "bronze" if "bronze" in self.df_medals.columns else "Bronze"
        tot_col = "total_medals" if "total_medals" in self.df_medals.columns else "Total_Medals"
        calc_total = self.df_medals[g_col] + self.df_medals[s_col] + self.df_medals[b_col]
        mismatches = (calc_total != self.df_medals[tot_col]).sum()
        self.assertEqual(mismatches, 0, f"Found {mismatches} arithmetic discrepancies in total medals")

    def test_05_usa_deduplicated_standings(self):
        """Verify USA official event medal tally matches 2,823 total and 1,131 Gold."""
        noc_col = "noc" if "noc" in self.df_medals.columns else "NOC"
        g_col = "gold" if "gold" in self.df_medals.columns else "Gold"
        tot_col = "total_medals" if "total_medals" in self.df_medals.columns else "Total_Medals"
        usa_records = self.df_medals[self.df_medals[noc_col] == "USA"]
        usa_gold = int(usa_records[g_col].sum())
        usa_tot = int(usa_records[tot_col].sum())
        self.assertEqual(usa_gold, 1131, f"USA Gold mismatch: expected 1131, got {usa_gold}")
        self.assertEqual(usa_tot, 2823, f"USA Total mismatch: expected 2823, got {usa_tot}")

    def test_06_processed_tables_exist(self):
        """Verify secondary processed benchmark tables exist."""
        self.assertTrue(os.path.exists(self.host_path), "host_nation_performance.csv missing")
        self.assertTrue(os.path.exists(self.efficiency_path), "regional_sports_efficiency.csv missing")
        self.assertTrue(os.path.exists(self.funding_path), "sports_funding_benchmark.csv missing")

    def test_07_host_nation_surge(self):
        """Verify host nation advantage surge rate is 86.7% and mean bump is +15.4 medals."""
        df_host = pd.read_csv(self.host_path)
        net_col = "medal_bump" if "medal_bump" in df_host.columns else "net_medal_bump"
        valid_bumps = df_host[net_col].dropna()
        surge_rate = (valid_bumps > 0).mean()
        mean_bump = valid_bumps.mean()
        self.assertGreaterEqual(surge_rate, 0.85, f"Host surge rate {surge_rate:.1%} is below 85%")
        self.assertAlmostEqual(mean_bump, 15.4, places=1, msg=f"Mean bump expected 15.4, got {mean_bump}")

    def test_08_funding_correlation(self):
        """Verify UK Sport funding correlation r > 0.70."""
        df_fund = pd.read_csv(self.funding_path)
        fund_col = [c for c in df_fund.columns if "fund" in c.lower() or "invest" in c.lower()][0]
        med_col = [c for c in df_fund.columns if "medal" in c.lower()][0]
        corr = df_fund[fund_col].corr(df_fund[med_col])
        self.assertGreater(corr, 0.70, f"Funding correlation {corr:.3f} is below 0.70")

    def test_09_tableau_workbook_exists(self):
        """Verify Tableau packaged workbook (.twbx) is present in Phase 5 / Development."""
        twbx_path = resolve_file([
            os.path.join(ROOT_DIR, "5. Project Development Phase", "Tableau Dashboard Development", "Global_Olympic_Sports_Performance_Analysis.twbx"),
            os.path.join(ROOT_DIR, "5. Project Development Phase", "tableau", "Global_Olympic_Sports_Performance_Analysis.twbx")
        ])
        self.assertTrue(os.path.exists(twbx_path), "Tableau .twbx file missing")
        self.assertGreater(os.path.getsize(twbx_path), 50000, "Tableau .twbx file is too small")

    def test_10_documentation_deliverables_exist(self):
        """Verify Project_Report.pdf and demo video exist in Phase 7."""
        pdf_path = resolve_file([
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Final Project Report", "Project_Report.pdf"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "reports", "Project_Report.pdf")
        ])
        mp4_path = resolve_file([
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Demo Video", "Olympic_Sports_Analysis_Demo_5_Minutes.mp4"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "Demo Video", "Project_Demo.mp4"),
            os.path.join(ROOT_DIR, "7. Documentation and Demo", "demo", "Project_Demo.mp4")
        ])
        self.assertTrue(os.path.exists(pdf_path), "Project_Report.pdf missing")
        self.assertTrue(os.path.exists(mp4_path), "Demo MP4 file missing")
        self.assertGreater(os.path.getsize(pdf_path), 500000, "PDF report size abnormal")
        self.assertGreater(os.path.getsize(mp4_path), 5000000, "MP4 file size abnormal")

if __name__ == "__main__":
    unittest.main()
