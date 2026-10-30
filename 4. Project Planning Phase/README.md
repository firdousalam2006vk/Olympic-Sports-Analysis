# Phase 4: Project Planning Phase
## Project Roadmap, Timeline & Development Methodology

---

## 🗺️ 1. Project Development Roadmap

The project followed the **Agile Data Analytics Lifecycle (CRISP-DM)** framework, structured into six sequential sprints:

```
Sprint 1: Problem Definition & Data Audit
├── Formulate research questions
├── Audit raw IOC archives
└── Identify the Team Multi-Counting Trap

Sprint 2: Data Engineering & Deduplication Pipeline
├── Construct clean_data.py
├── Implement deterministic event deduplication
└── Optimize athletes.csv to <25 MB for GitHub

Sprint 3: Statistical Modeling & Hypothesis Testing
├── Build analyze.py
├── Calculate host nation advantage moving baseline
└── Model UK Sport high-performance capital ROI

Sprint 4: Business Intelligence & Tableau Public
├── Build calculated fields and LOD expressions
├── Construct Dashboard 1 (Global Performance)
├── Construct Dashboard 2 (Regional Efficiency)
└── Publish to Tableau Public cloud

Sprint 5: Full-Stack Web Application (Olympic-Flask)
├── Architect Flask backend (app.py)
├── Develop responsive templates (Jinja2 + Bootstrap)
└── Expose REST API endpoints for dynamic querying

Sprint 6: Quality Assurance, Testing & Executive Reporting
├── Run 10-point automated unit test suite
├── Run 20-point quality assurance audit
├── Render 11-page publication-quality PDF report
└── Compile 1080p Full HD demonstration video
```

---

## 📅 2. Timeline & Gantt Chart

```
+-------------------------------------------------------------------------------+
| PHASE / SPRINT                  | SPRINT 1 | SPRINT 2 | SPRINT 3 | SPRINT 4 | SPRINT 5 | SPRINT 6 |
+---------------------------------+----------+----------+----------+----------+----------+----------+
| 1. Ideation & Scoping           |  [████]  |          |          |          |          |          |
| 2. Requirement Analysis         |  [████]  |          |          |          |          |          |
| 3. System & UI Design           |          |  [████]  |          |          |          |          |
| 4. Data Pipeline & Deduplication|          |  [████]  |          |          |          |          |
| 5. Statistical Modeling & EDA   |          |          |  [████]  |          |          |          |
| 6. Tableau Dashboard Authoring  |          |          |          |  [████]  |          |          |
| 7. Olympic-Flask Development    |          |          |          |          |  [████]  |          |
| 8. Testing & Quality Assurance  |          |          |          |          |          |  [████]  |
| 9. PDF Report & Video Delivery  |          |          |          |          |          |  [████]  |
+-------------------------------------------------------------------------------+
```

---

## 👥 3. Task Allocation (RACI Matrix)

| Milestone Deliverable | Data Analyst | Python Engineer | Tableau Developer | QA Specialist |
| :--- | :---: | :---: | :---: | :---: |
| Problem Statement & Ideation | **Accountable** | Consulted | Consulted | Informed |
| Deduplication Algorithm Design | Consulted | **Responsible** | Informed | Verified |
| Storage Optimization (<25 MB) | Informed | **Responsible** | Informed | Verified |
| Tableau Dashboard Construction | Consulted | Informed | **Responsible** | Verified |
| Flask Web Application | Consulted | **Responsible** | Consulted | Verified |
| Test Suite & System Audit | Informed | Consulted | Consulted | **Responsible** |
| Final Academic PDF Report | **Responsible** | Consulted | Consulted | Verified |

---

## ⚙️ 4. Risk Assessment & Mitigation Matrix

| Identified Risk | Severity | Probability | Mitigation Strategy Implemented |
| :--- | :---: | :---: | :--- |
| **GitHub 25MB Web Upload Limit** | High | High | Focused `athletes.csv` on Modern Era (1980–2016) with clean integer biometrics (22.78 MB); preserved full archive in `athletes_all_1896_2016.csv.gz` (5.25 MB). |
| **Team Event Multi-Counting** | Critical | High | Engineered deterministic event deduplication grouping by `[games_id, noc, sport, event, medal]`. |
| **Dual-City Host Conflict (1956)** | Medium | Medium | Mapped Melbourne as primary host city in `clean_data.py`, reducing duplicate primary keys to exactly 0. |
| **Speculative Data Fabrication** | Critical | Medium | Zero simulated values; used UK Sport official published lottery grants as audited high-performance benchmark. |

