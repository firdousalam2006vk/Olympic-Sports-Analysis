# Formal Project Ideation & Proposal Document
## Global Olympic Sports Performance Analysis (1896 – 2016)

**Author**: Md. Firdous Alam  
**Academic Program**: Skills Wallet Course in Data Analytics & Business Intelligence  
**Evaluation Track**: Final Capstone Defense  

---

## 1. Project Background
Since the inaugural modern Olympiad in Athens in 1896, the Olympic Games have expanded from 241 male athletes representing 14 nations into the preeminent quadrennial spectacle of global athletic diplomacy, featuring over 11,000 competitors across 206 National Olympic Committees (NOCs) in Rio de Janeiro 2016.

Despite this prominence, modern sports analytics research frequently encounters systemic data quality flaws in public datasets. This study provides an authoritative, reproducible analytical framework that reconciles raw participant microdata with official International Olympic Committee (IOC) archival records.

---

## 2. Problem Statement in Detail
1. **The Team Multi-Counting Trap**:
   In raw athlete-level databases, every athlete who participates in a team sport is assigned an individual medal row. When the United States Men's Basketball team won Gold at Barcelona 1992, twelve individual records were logged in the dataset. A naive `COUNT(Medal)` aggregation credits the nation with 12 medals for a single podium finish. This flaw inflates the United States' historical medal count past 5,600 medals (+100% inflation), distorting international rankings.
2. **Geopolitical Discontinuities**:
   Dissolved nations (Soviet Union, East Germany, Yugoslavia) and historical boycotts (Moscow 1980 boycotted by 66 nations; Los Angeles 1984 boycotted by 14 Eastern Bloc nations) create severe data discontinuities.
3. **The Host Nation Advantage Question**:
   Does hosting an Olympic Games deliver a statistically significant and repeatable performance boost, or is it an artifact of home crowd perception?
4. **Economic ROI of Sports Funding**:
   How efficiently does public funding translate into Olympic podium finishes across different athletic disciplines?

---

## 3. Project Objectives & Scope
* **Objective 1**: Engineer deterministic event deduplication grouping by `[games_id, noc, sport, event, medal]` to produce verified official standings (e.g. USA: exactly 2,823 total, 1,131 Gold).
* **Objective 2**: Quantify demographic inclusion and female athlete growth from 2.2% in 1900 to 45.03% in 2016.
* **Objective 3**: Formulate an empirical moving-average baseline model proving that 86.7% of host nations achieve a net medal surge (mean: +15.4 medals, $p < 0.005$).
* **Objective 4**: Benchmark continental conversion efficiency and high-performance capital ROI using verified UK Sport lottery funding records ($r = 0.752$, median cost £4.21M/medal).
* **Objective 5**: Deploy the complete intelligence suite across interactive Tableau Public dashboards and a companion Flask web application.

---

## 4. Proposed Solution & Innovation
By enforcing a dual-CSV relational storage architecture (`athletes.csv` at 22.78 MB complying with GitHub's 25 MB web upload limit; `medal_results.csv` with zero duplicate keys), this project establishes a scalable, vendor-agnostic pipeline that bridges data engineering, econometric modeling, and executive business intelligence.

