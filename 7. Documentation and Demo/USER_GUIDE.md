# Tableau Public User Guide
# Global Olympic Sports Performance Analysis

**Project**: Global Olympic Sports Performance Analysis  
**Author**: Md. Firdous Alam  
**Live Tableau Public URL**: [https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3](https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3)  
**Packaged Workbook Location**: `tableau/Global_Olympic_Sports_Performance_Analysis.twbx`  

---

## 🎯 Purpose of this Guide

This user guide provides instructions on how to interact with, filter, and interpret the two production-grade dashboards published on Tableau Public. Whether you are viewing the live dashboard in a web browser or opening the packaged `.twbx` workbook in Tableau Desktop, this guide explains each visual component, filter action, and analytical metric.

---

## 🌐 Accessing the Dashboards

### Option 1: Live Web Browser Access (Recommended)
1. Open any modern web browser (Chrome, Edge, Firefox, Safari).
2. Navigate to: [https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3](https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3).
3. The dashboard loads directly on Tableau Public without requiring any software installation or sign-in.
4. For the best viewing experience, click the **Full Screen** icon in the bottom-right corner of the Tableau toolbar.

### Option 2: Offline Access via Tableau Desktop / Tableau Reader
1. Open **Tableau Desktop** or the free **Tableau Reader**.
2. Go to **File -> Open...** (or press `Ctrl + O`).
3. Select `tableau/Global_Olympic_Sports_Performance_Analysis.twbx` from your project folder.
4. The packaged extract (`.hyper`) and pre-configured calculated fields load automatically with zero configuration.

---

## 📊 DASHBOARD 1: Global Sports Performance Analytics Dashboard

Dashboard 1 provides a macro-historical perspective on participation scale, national podium dominance, and sport-specific conversion efficiency.

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Global Sports Performance Analytics Dashboard | 1896 – 2016 Historical Audit            |
+---------------------------------------------------------------------------------------------------+
|  [KPI 1: 51 Editions]  |  [KPI 2: 230 Nations]  |  [KPI 3: 135,571 Athletes]  |  [KPI 4: 18,905 Medals] |
+-------------------------------------------------------------+-------------------------------------+
|  VISUAL 1: Total Medal Achievements Across Nations          |  VISUAL 2: Trend of Medals Over Time|
|  (Horizontal Stacked Bar: Gold, Silver, Bronze)             |  (Dual-Line: Summer vs. Winter)     |
+-------------------------------------------------------------+-------------------------------------+
|  VISUAL 3: Avg Medals per Athlete by Sport Category         |  VISUAL 4: Country-Wise Breakdown   |
|  (Ranked Sport Efficiency & Powerhouse Dominance)           |  (Participation vs. Podium Results) |
+---------------------------------------------------------------------------------------------------+
|  INTERACTIVE FILTERS: [Season: All] | [Year Range Slider: 1896-2016] | [Country / NOC: All]        |
+---------------------------------------------------------------------------------------------------+
```

### Visual Components & Interpretation

#### 1. Executive KPI Cards (Top Banner)
* **Total Games / Editions (51)**: Encompasses all 29 modern Summer Games (1896 Athens to 2016 Rio) and 22 modern Winter Games (1924 Chamonix to 2014 Sochi).
* **Participating Nations (230)**: Total National Olympic Committees (NOCs) that have fielded teams.
* **Athletes Evaluated (135,571)**: Total unique Olympians registered in Olympic history.
* **Official Medals Awarded (18,905)**: Verified, deduplicated event-level podium finishes (6,195 Gold, 6,163 Silver, 6,547 Bronze).

#### 2. Total Medal Achievements Across Nations (Horizontal Stacked Bar)
* **What it shows**: The all-time top Olympic powers, segmented by medal tier.
  * **Gold**: Yellow / Golden bar segment.
  * **Silver**: Grey / Silver bar segment.
  * **Bronze**: Bronze / Copper bar segment.
* **How to interact**:
  * Hover over any bar to view the exact medal counts and all-time weighted score.
  * Click on a country (e.g., *United States*) to filter the accompanying yearly trend chart to show only that nation's historical timeline!

#### 3. Trend of Total Medals & Participation Over the Years (Line Chart)
* **What it shows**: The growth of the Olympic movement from 241 athletes in 1896 to 11,179 in 2016.
* **Key Observations**:
  * Notice the sharp drops in 1916, 1940, and 1944 (cancellations due to WWI and WWII).
  * Notice the dip in Moscow 1980 (Western boycott) and Los Angeles 1984 (Soviet boycott).
  * Observe the separation of Summer and Winter Games into alternating two-year cycles beginning in 1994 (Lillehammer).

#### 4. Avg Medals per Athlete by Sport Category (Sport Efficiency)
* **What it shows**: The relative conversion rate of medals won per athlete across major disciplines (Athletics, Swimming, Gymnastics, Wrestling, Rowing, Cycling).
* **Key Insights**: Shows which sports yield the highest podium returns for specialized delegations.

---

## 📈 DASHBOARD 2: Olympic Performance & Regional Efficiency Dashboard

Dashboard 2 is designed for sports economists and high-performance directors, focusing on continental equity, host nation advantage, and capital investment returns.

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Olympic Performance and Regional Efficiency Dashboard                                   |
+---------------------------------------------------------------------------------------------------+
|  VISUAL 5: Medal Share by Region (Donut / Pie)              |  VISUAL 6: Avg Medal Efficiency     |
|  (Americas, Europe, Asia, Oceania, Africa)                  |  (Medals won per 100 Athletes)      |
+-------------------------------------------------------------+-------------------------------------+
|  VISUAL 7: The Host Nation Advantage (Host Bump)            |  VISUAL 8: Sports Investment vs ROI |
|  (Grouped Bar: Pre-Host vs. Host Year vs. Post-Host)        |  (Scatter: Funding £M vs. Medals)   |
+---------------------------------------------------------------------------------------------------+
|  FILTERS: [Continent Selector] | [Host Status: Host vs. Visitor] | [Funding Cycle: Rio 2016]      |
+---------------------------------------------------------------------------------------------------+
```

### Visual Components & Interpretation

#### 1. Medal Share by Region (Donut Chart)
* **What it shows**: Geographic distribution of all 18,905 historical Olympic medals.
* **Key Finding**: Europe (63.4%) and the Americas (21.0%) account for **84.4%** of all Olympic medals awarded in history, illustrating the transatlantic concentration of sports infrastructure.

#### 2. Average Medal Efficiency by Region (Bar Chart)
* **Metric**: Medals won per 100 entered athletes.
  * **Americas**: `10.96%`
  * **Europe**: `10.94%`
  * **Asia**: `8.13%`
  * **Oceania**: `8.11%`
  * **Africa**: `4.00%`
* **Interpretation**: Eliminates delegation size bias. Africa's 4.00% rate reflects structural exclusion from capital-intensive sports (swimming pools, velodromes, gymnastics halls), despite world-class endurance running supremacy.

#### 3. Medal Totals Across Olympic Hosts (The Host Bump)
* **What it shows**: Side-by-side performance of host nations across three consecutive editions:
  * **Pre-Host Games ($t-1$)**: Baseline performance.
  * **Host Year ($t=0$)**: Performance during home celebration.
  * **Post-Host Games ($t+1$)**: Retention or hangover performance.
* **Key Finding**: **86.7% of host nations achieve an immediate medal surge**, averaging **+15.4 net medals**.
* **Notable Surges**:
  * Spain 1992: 4 $\rightarrow$ 22 medals (+450.0%)
  * China 2008: 63 $\rightarrow$ 100 medals (+58.7%)
  * Great Britain 2012: 48 $\rightarrow$ 65 medals (+35.4%)

#### 4. Sports Investment vs. Medal Performance (Scatter Plot)
* **Data Source**: UK Sport official published High Performance Strategy allocations for Rio 2016.
* **Axes**:
  * **X-Axis**: High-Performance Funding (£ Millions).
  * **Y-Axis**: Olympic Medals Won.
* **Key Trend**: A strong positive correlation ($r = 0.752, R^2 = 0.566$).
* **Efficiency Tiers**:
  * *High Efficiency (< £2.5M/medal)*: Triathlon (£1.83M), Shooting (£1.98M), Gymnastics (£2.09M).
  * *Capital Intensive (> £6.0M/medal)*: Rowing (£6.52M), Sailing (£8.50M), Hockey (£16.11M).

---

## 🎛️ Interactive Filtering & Cross-Filtering Techniques

Both dashboards feature responsive bidirectional cross-filtering:

1. **Filtering by Season (`Summer` vs. `Winter`)**:
   * Use the Season dropdown in the top-right filter shelf.
   * Selecting `Winter` dynamically shifts country standings to Norway, Germany, the US, and Austria, highlighting cold-climate specialization.
2. **Year Range Slider**:
   * Drag the slider handles to isolate specific historical periods (e.g., Modern Era: `1980 – 2016` or Cold War: `1952 – 1988`).
3. **One-Click Mark Selection**:
   * Click on any country name in Visual 1.
   * Companion charts automatically update to isolate that country's longitudinal trajectory.
   * Click the selected bar again to clear the filter.

---

## ❓ Frequently Asked Questions & Troubleshooting

### Q1: Why do US medal counts in this dashboard show 2,823 medals instead of 5,600+?
**Answer**: Raw athlete datasets list one row per athlete. When an 8-person rowing crew or a 22-player football squad wins a medal, raw datasets count 8 or 22 rows. Our deterministic pipeline deduplicates team events by `[year, season, sport, event, medal, noc]`, exactly matching the International Olympic Committee's official medal records.

### Q2: What if Tableau prompts "Could not find the referenced data source"?
**Answer**: If opening the `.twb` file on a new computer:
1. Click **Locate...** on the prompt.
2. Select `data/medal_results.csv` from the project directory.
3. Tableau reconnects all fields and calculated measures automatically. (Alternatively, open `tableau/Global_Olympic_Sports_Performance_Analysis.twbx` which embeds the data extract directly).

### Q3: How do I export a high-resolution PDF or image from Tableau Public?
**Answer**:
1. In the top-right or bottom toolbar of the Tableau Public browser view, click the **Download** icon.
2. Select **Image** (PNG) or **PDF**.
3. Choose layout orientation and click **Generate** to save publication-ready visuals.

