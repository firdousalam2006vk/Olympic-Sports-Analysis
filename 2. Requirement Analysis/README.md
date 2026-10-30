# Phase 2: Requirement Analysis
## Software Requirements Specification (SRS) Summary

---

## 📋 1. Functional Requirements (FR)

| Req ID | Requirement Title | Detailed Description | Verification Method |
| :---: | :--- | :--- | :--- |
| **FR-01** | Raw Ingestion & Formatting | System must ingest 120 years of historical Olympic competition data and coerce data types without data loss. | Unit Test & Checksum |
| **FR-02** | Team Event Deduplication | System must collapse multi-player rosters in team events to strictly 1 medal per event per nation. | Key Match against IOC |
| **FR-03** | Primary Key Uniqueness | Processed dataset `medal_results.csv` must maintain 0 duplicate primary keys across `[games_id, noc]`. | Python Unit Test |
| **FR-04** | GitHub File Size Limit | Output dataset `athletes.csv` must remain strictly below 25.0 MB (25,000,000 bytes) for web upload compatibility. | Byte-size Assertion |
| **FR-05** | Demographic Modeling | Pipeline must calculate gender participation percentages per edition and track modern shifts (1980–2016). | Tabular Aggregation |
| **FR-06** | Host Nation Surge Benchmark | System must compute pre-host moving averages and calculate net medal gain for all host nations. | Statistical Formula |
| **FR-07** | High-Performance ROI Model | Pipeline must calculate Pearson correlation and cost per medal (£M) for UK Sport lottery investments. | SciPy/Pandas Correlation |
| **FR-08** | Interactive BI Dashboards | Tableau Public workbooks must provide interactive slicers for Season, Year range, and Nation. | Functional UX Test |
| **FR-09** | Web Application Portal | Flask web application must serve responsive templates with live search, filters, and JSON REST APIs. | Flask Test Client |

---

## ⚡ 2. Non-Functional Requirements (NFR)

* **NFR-01: Accuracy & Integrity**: Zero fabricated records or hallmarked statistics. Deduplicated totals must match official IOC archives (e.g. USA: 2,823 total, 1,131 Gold).
* **NFR-02: Performance**: Data transformation pipelines must execute end-to-end in under 15 seconds on commodity hardware.
* **NFR-03: Portability & Standards**: All tabular exchanges must utilize vendor-agnostic CSV format; web app must run on Python 3.10+.
* **NFR-04: Usability**: Tableau dashboards and Flask web interfaces must conform to responsive UI standards with an executive Olympic Navy/Gold design palette.
* **NFR-05: Reproducibility**: 100% of pipeline stages must execute via automated, version-controlled scripts without manual spreadsheet edits.

---

## 💻 3. Hardware and Software Requirements

### Hardware Specifications
* **Processor**: Intel Core i3 / AMD Ryzen 3 or higher (Tested on multi-core x64).
* **RAM**: 4 GB minimum (8 GB recommended for memory-mapped Pandas operations).
* **Disk Space**: 500 MB free storage for datasets, generated charts, PDF reports, and video assets.

### Software Specifications
* **Operating System**: Windows 10/11, macOS Monterey+, or Linux (Ubuntu 20.04+).
* **Runtime**: Python 3.10 to 3.14 (Tested on Python 3.14.0).
* **BI Suite**: Tableau Desktop / Tableau Public 2023.x or 2024.x.
* **Web Framework**: Flask 3.1.3 + Jinja2 + Werkzeug.

---

## 🛠️ 4. Tools and Technologies Stack

```
Data Ingestion & ETL      : Python 3.14, Pandas 3.1.0, NumPy 2.4.6
Exploratory Data Analysis : Jupyter Notebook, IPython Kernel, Matplotlib, Seaborn
Business Intelligence    : Tableau Public Desktop & Cloud Web Authoring
Web Application Portal   : Python Flask 3.1.3, HTML5, CSS3 (Olympic Theme), JavaScript
Presentation & Media     : python-pptx 1.0.2, OpenCV 5.0.0, Pillow 12.0.0, ReportLab 5.1.0
Testing & Verification   : Python unittest, pytest 8.0+
Version Control          : Git, GitHub
```

---

## 📊 5. Dataset Requirements & Schema Specifications
* **Input Dataset**: Historical Olympic competition entries (1896–2016, 271,116 rows).
* **Normalized Outputs**:
  1. `athletes.csv`: 157,417 rows × 18 columns (Modern Era 1980–2016; size = 22.78 MB).
  2. `medal_results.csv`: 3,837 rows × 17 columns (51 editions; size = 301.8 KB; zero duplicate primary keys).

