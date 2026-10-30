# Project Execution & Sprint Management Plan
## Global Olympic Sports Performance Analysis

---

## 1. Development Methodology: CRISP-DM
This project adopted the **Cross-Industry Standard Process for Data Mining (CRISP-DM)**, adapted for reproducible sports business intelligence:

1. **Business & Domain Understanding**:
   - Identified the team event multi-counting flaw in existing public dashboards.
   - Defined target KPIs: Total Editions (51), Deduplicated Medals (18,905), USA Medals (2,823).
2. **Data Understanding**:
   - Explored raw archives from Sports-Reference / Kaggle.
   - Identified the 25 MB GitHub web upload constraint.
3. **Data Preparation**:
   - Filtered `athletes.csv` to Modern Olympic Era (1980–2016) with integer biometrics (22.78 MB).
   - Produced `medal_results.csv` with zero duplicate keys across 3,837 rows.
4. **Modeling & Hypothesis Testing**:
   - Formulated the Host Nation Advantage moving baseline (+15.4 medals net bump).
   - Modelled sports funding returns using UK Sport Rio 2016 outturn ($r = 0.752$).
5. **Evaluation**:
   - Automated 10-point unit test suite and 20-point quality assurance verification (100% pass rate).
6. **Deployment**:
   - Published live on Tableau Public Cloud.
   - Engineered companion Flask web application with search and REST APIs.

---

## 2. Sprint Deliverables Checklist

- [x] **Sprint 1**: Ideation, Problem Statement, and Architecture Design.
- [x] **Sprint 2**: Ingestion pipeline, deduplication algorithm, and schema testing.
- [x] **Sprint 3**: Statistical audit, host bump modeling, and funding ROI calculations.
- [x] **Sprint 4**: Tableau Public dual dashboard construction and cloud publication.
- [x] **Sprint 5**: Olympic-Flask web portal development and API route validation.
- [x] **Sprint 6**: 1080p demo video compilation and 11-page publication-quality PDF report generation.

