# Phase 5: Project Development Phase
## Source Code, Curated Datasets, Notebooks & Tableau Workbooks

---

## 📌 Development Overview
This phase houses the production-ready source code, relational datasets, interactive exploration notebooks, and Tableau Public business intelligence workbooks.

---

## 📂 Subdirectory Organization

### 1. `src/` (Python Source Engines)
* [`clean_data.py`](src/clean_data.py): The primary data ingestion, type coercion, and event-deduplication script. Outputs `athletes.csv` (< 25 MB) and `medal_results.csv` (0 duplicate keys).
* [`analyze.py`](src/analyze.py): The core statistical analysis engine calculating all-time nation rankings, weighted scores, gender ratios, host bumps, and continental efficiency.
* [`exploratory_analysis.py`](src/exploratory_analysis.py): Standalone script running automated statistical distributions and saving JSON audits.

### 2. `data/` (Curated & Processed Data Tables)
* [`athletes.csv`](data/athletes.csv): Curated Modern Era dataset (1980–2016; 157,417 rows × 18 columns; **22.78 MB**, strictly under GitHub's 25 MB limit).
* [`medal_results.csv`](data/medal_results.csv): Official deduplicated country-edition aggregates across all 51 Olympic editions (1896–2016; 3,837 rows; **0 duplicate keys**).
* [`athletes_all_1896_2016.csv.gz`](data/athletes_all_1896_2016.csv.gz): Full historical compressed archive (1896–2016; 271,116 rows; 5.25 MB).
* [`raw/`](data/raw/): Authentic raw source files (`olympics_raw.csv`, `noc_regions_raw.csv`).
* [`processed/`](data/processed/): Benchmark tables (`host_nation_performance.csv`, `regional_sports_efficiency.csv`, `sports_funding_benchmark.csv`).

### 3. `notebooks/` (Interactive Exploration)
* [`Olympic_Sports_Performance_Analysis.ipynb`](notebooks/Olympic_Sports_Performance_Analysis.ipynb): Complete end-to-end interactive Jupyter Notebook covering data loading, deduplication validation, top-nation aggregation, female participation modeling, host nation surge tests, and funding ROI scatter plots.

### 4. `tableau/` (Visual Analytics Suite)
* [`Global_Olympic_Sports_Performance_Analysis.twbx`](tableau/Global_Olympic_Sports_Performance_Analysis.twbx): Packaged Tableau Public workbook containing embedded hyper extracts and both complete dashboards.
* [`Olympic_Performance_Analysis.twb`](tableau/Olympic_Performance_Analysis.twb): Native XML Tableau Public workbook connected to `medal_results.csv`.
* [`TABLEAU_BUILD_GUIDE.md`](tableau/TABLEAU_BUILD_GUIDE.md): Step-by-step workbook layout manual.
* [`Calculated_Fields_Reference.md`](tableau/Calculated_Fields_Reference.md): Formulas for LODs and KPI tiles.
* [`Tableau_Data_Dictionary.md`](tableau/Tableau_Data_Dictionary.md): Entity relationship schema & attribute definitions.

---

## ⚡ Execution Commands
```bash
# Run data cleaning & deduplication
python "5. Project Development Phase/src/clean_data.py"

# Run exploratory and confirmatory analysis
python "5. Project Development Phase/src/analyze.py"
```

