# Tableau Public Complete Build Guide: Global Olympic Performance Analysis

This guide provides an exact, click-by-click instruction set to assemble two executive-level dashboards and an analytical story in Tableau Public.

---

## 🎨 Professional Design System & Color Palette

To achieve a modern, institutional look:

| Element | Hex Code | Visual Preview / Description |
| :--- | :--- | :--- |
| **Primary Navy** | `#1B365D` | Headers, KPI titles, primary bars, main borders |
| **Slate Blue** | `#2E6B9E` | Secondary series, winter trends, active highlights |
| **Olympic Gold** | `#D4AF37` | Gold medals, key callouts, benchmark lines |
| **Olympic Silver** | `#A0AAB2` | Silver medal category |
| **Olympic Bronze**| `#CD7F32` | Bronze medal category |
| **Canvas Background** | `#F8FAFC` | Dashboard canvas & sheet background |
| **Card / Container BG**| `#FFFFFF` | Individual KPI cards and chart containers |
| **Subtle Border** | `#E2E8F0` | Container outlines, divider lines |
| **Dark Typography**| `#1E293B` | Titles, axes labels, primary text |

---

## 🚀 Quick Start: Data Source Connection

1. Open **Tableau Public** (Desktop app or browser web authoring).
2. Under **Connect** -> Click **Text File**.
3. Navigate to `data/processed/` and select **`medal_results.csv`**.
4. In the Data Source canvas, verify field types:
   - `year`: Number (whole)
   - `country`: String -> Click data type icon -> **Geographic Role** -> **Country/Region**
   - `is_host`: Number (whole)
   - `total_medals`, `gold`, `silver`, `bronze`, `athletes_count`: Number (whole)
5. To add the investment dataset:
   - Click **Add** next to Connections -> **Text File** -> Select **`sports_funding_benchmark.csv`**.

---

# 📊 DASHBOARD 1: Global Olympic Performance

**Dimensions**: `1366 x 768 px` (Fixed Layout) or `Automatic`.  
**Objective**: High-level macro perspective of modern Olympic history, nation medal standings, seasonal expansion, and medal composition.

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Global Olympic Performance Analysis | All-Time Historical Audit (1896-2016)              |
+---------------------------------------------------------------------------------------------------+
|  [KPI 1: 51 Editions]  |  [KPI 2: 135,571 Athletes]  |  [KPI 3: 18,905 Medals]  |  [KPI 4: 230 NOCs]  |
+-------------------------------------------------------------+-------------------------------------+
|  SHEET 1: All-Time Medal Table by Country (Top 15)          |  SHEET 2: Olympic Expansion Trend   |
|  (Horizontal Stacked Bar: Gold, Silver, Bronze)             |  (Dual-Line: Summer vs. Winter)     |
|                                                             |                                     |
+-------------------------------------------------------------+-------------------------------------+
|  SHEET 3: Global Medal Distribution (Geographic Map)        |  SHEET 4: Medal Quality Breakdown   |
|  (Filled Map / Choropleth by Country Medals)                |  (Donut / Stacked Bar by Type)      |
+---------------------------------------------------------------------------------------------------+
|  FILTERS BAR: [Season: All] | [Year Slider: 1896-2016] | [Continent: All] | [Host Filter: All]    |
+---------------------------------------------------------------------------------------------------+
```

---

### Step-by-Step Worksheet Construction for Dashboard 1

#### Worksheet 1.1: KPI Cards (`W1_KPI_Cards`)
1. Create a new sheet named `W1_KPI_Cards`.
2. Drag `Measure Values` to **Text** on the Marks card.
3. Remove all measures except:
   - `Distinct Count(games_id)` -> Alias: **Total Editions** (Value: `51`)
   - `Sum(athletes_count)` -> Alias: **Athlete Participations** (Value: `197k+` / `135,571` unique)
   - `Sum(total_medals)` -> Alias: **Official Medals** (Value: `18,905`)
   - `Distinct Count(noc)` -> Alias: **Competing Nations** (Value: `230`)
4. Change mark type to **Square** or format as 4 separate mini-cards.
5. In **Label / Text**: Set font to `Arial Bold`, size `22pt`, color `#1B365D`. Set subtitle to `10pt`, `#64748B`.

#### Worksheet 1.2: Country Medal Standings (`W1_Country_Medals`)
1. Create a new sheet named `W1_Country_Medals`.
2. Drag `country` to **Rows**.
3. Drag `Measure Values` to **Columns**.
4. In the **Measure Values** card, retain only:
   - `SUM(bronze)`
   - `SUM(silver)`
   - `SUM(gold)`
5. Drag `Measure Names` to **Color** on the Marks card.
6. Edit Colors:
   - `SUM(gold)` -> `#D4AF37`
   - `SUM(silver)` -> `#A0AAB2`
   - `SUM(bronze)` -> `#CD7F32`
7. Click the sort icon on `country` -> Sort descending by `SUM(total_medals)`.
8. Right-click `country` on Rows -> **Filter** -> Top tab -> **Top 15** by `SUM(total_medals)`.
9. Right-click the horizontal axis -> Add Reference Line or add total labels to show full medals.
10. Remove vertical grid lines, format row headers to `#1E293B`, Bold 10pt.

#### Worksheet 1.3: Olympic Growth & Longitudinal Trend (`W1_Year_Trend`)
1. Create a new sheet named `W1_Year_Trend`.
2. Drag `year` to **Columns** (ensure it is continuous or discrete year).
3. Drag `SUM(athletes_count)` to **Rows**.
4. Drag `season` to **Color**.
5. Set Colors:
   - `Summer` -> Primary Navy `#1B365D`
   - `Winter` -> Slate Blue `#2E6B9E`
6. Add Mark Labels for peak years (e.g., 2016 Summer: 11,179 athletes).
7. Format background to `#F8FAFC`, line thickness to 2.5pt.

#### Worksheet 1.4: Global Medal Map (`W1_World_Map`)
1. Create a new sheet named `W1_World_Map`.
2. Double-click `country` (Tableau automatically generates Latitude and Longitude).
3. Drag `SUM(total_medals)` to **Color**.
4. Click **Color** -> Edit Colors -> Palette: **Custom Sequential** -> Light Slate (`#CBD5E1`) to Deep Navy (`#1B365D`).
5. Drag `country`, `SUM(gold)`, `SUM(silver)`, `SUM(bronze)`, `SUM(total_medals)` to **Tooltip**.
6. Set Map Layers: **Light** style, uncheck unnecessary borders.

---

# 📊 DASHBOARD 2: Sports and Regional Efficiency

**Dimensions**: `1366 x 768 px` (Fixed Layout).  
**Objective**: Deep comparative analysis of sports specialization, continental efficiency (conversion rate), host nation advantage, and capital investment efficiency.

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Sports & Regional Efficiency | Host Nation Advantage & Investment Modeling               |
+---------------------------------------------------------------------------------------------------+
|  SHEET 5: Continental Efficiency Analysis                   |  SHEET 6: The "Host Nation Advantage"  |
|  (Bar Chart: Medals per 100 Athletes by Continent)          |  (Grouped Bar: Pre vs. Host vs. Post) |
|                                                             |                                     |
+-------------------------------------------------------------+-------------------------------------+
|  SHEET 7: Top 10 Sports & Dominant Nations                  |  SHEET 8: Capital vs. Podium ROI    |
|  (Ranked Bar: Athletics, Swimming, Gymnastics, etc.)        |  (Scatter: UK Sport £M vs. Medals)  |
+---------------------------------------------------------------------------------------------------+
|  FILTERS: [Cycle: Rio 2016] | [Continent: All] | [Sport Type: All]                                |
+---------------------------------------------------------------------------------------------------+
```

---

### Step-by-Step Worksheet Construction for Dashboard 2

#### Worksheet 2.1: Continental Conversion Efficiency (`W2_Regional_Efficiency`)
1. Create a new sheet named `W2_Regional_Efficiency`.
2. Drag `continent` to **Columns**.
3. Drag `[CF_Medal_Conversion_Rate]` to **Rows** (Formula: `(SUM(total_medals) / SUM(athletes_count)) * 100`).
4. Filter out `'Other'` and `'Special'` continents.
5. Drag `continent` to **Color** (Palette: Navy, Slate, Sky Blue, Gold, Orange).
6. Click **Label** -> Check **Show mark labels** (Format as `0.00%`).
7. Result:
   - Americas: `10.96%`
   - Europe: `10.94%`
   - Asia: `8.13%`
   - Oceania: `8.11%`
   - Africa: `4.00%`

#### Worksheet 2.2: Host Nation Advantage Comparison (`W2_Host_Nation_Advantage`)
1. Connect to `host_nation_performance.csv`.
2. Create a new sheet named `W2_Host_Nation_Advantage`.
3. Drag `country` and `host_year` to **Columns**.
4. Drag `Measure Values` to **Rows**.
5. Keep only:
   - `SUM(pre_medals)`
   - `SUM(host_medals)`
   - `SUM(post_medals)`
6. Drag `Measure Names` to **Color**:
   - `pre_medals` -> Silver `#A0AAB2`
   - `host_medals` -> Deep Navy `#1B365D`
   - `post_medals` -> Slate Blue `#2E6B9E`
7. Mark Type: **Bar** (Side-by-side grouped bar).
8. Highlight key surges: China 2008 (+37 medals), Spain 1992 (+18 medals), Great Britain 2012 (+17 medals).

#### Worksheet 2.3: Top Sports & Historical Dominance (`W2_Top_Sports`)
1. Connect to `athletes.csv` (or use aggregated sports summary).
2. Filter for `medal != 'No Medal'`.
3. Drag `sport` to **Rows**, sorted descending by `COUNT(event)`.
4. Keep **Top 10 Sports**: Athletics, Swimming, Gymnastics, Wrestling, Shooting, Boxing, Cycling, Fencing, Canoeing, Rowing.
5. Drag `country` (or `team`) to **Color** or add to **Tooltip** to reveal dominant powerhouse (e.g., USA in Swimming/Athletics, Germany in Canoeing/Rowing).

#### Worksheet 2.4: High-Performance Funding vs. Medals Scatter (`W2_Investment_Scatter`)
1. Connect to `sports_funding_benchmark.csv`.
2. Filter for `cycle = 'Rio 2016'`.
3. Drag `funding_millions_gbp` to **Columns**.
4. Drag `medals_won` to **Rows**.
5. Drag `sport` to **Detail** and **Label**.
6. Drag `funding_millions_gbp` to **Size** on Marks card.
7. Change Mark Type to **Circle**, color `#1B365D`, border white, opacity 85%.
8. Right-click canvas -> **Trend Lines** -> Check **Show Trend Lines** (displays linear fit, $r = 0.752$).
9. Add Caption: *"Data Source: UK Sport Official Published High Performance Allocations vs. Rio 2016 Medals"*.

---

## 🧭 Dashboard Assembly & Container Hierarchy

### Step 1: Set Canvas Size
- In the Dashboard pane (bottom-left), set **Size** to **Fixed size: Generic Desktop (1366 x 768)**.

### Step 2: Container Layout
1. Drag a **Vertical Layout Container** onto the blank dashboard.
2. Inside it, drag a **Horizontal Layout Container** at the very top for the **Header Title & Subtitle**.
   - Background: Deep Navy `#1B365D`.
   - Text: White bold 18pt: *"Global Olympic Sports Performance Analysis"*.
   - Subtitle: Light Gray 10pt: *"Skills Wallet Course Academic Project | Tableau Public Edition"*.
3. Below the header, drag a **Horizontal Layout Container** for the **4 KPI Cards**.
   - Set outer padding: 6px, inner padding: 8px.
   - Background: White `#FFFFFF`, Border: 1px solid `#E2E8F0`.
4. Below the KPIs, drag a **Horizontal Layout Container** split into two columns:
   - Left: `W1_Country_Medals` (Width: 55%).
   - Right: `W1_Year_Trend` (Width: 45%).
5. Below that, drag another Horizontal split:
   - Left: `W1_World_Map` (Width: 60%).
   - Right: `W1_Regional_Efficiency` or `W1_Medal_Breakdown` (Width: 40%).

### Step 3: Interactive Dashboard Actions
1. Go to **Dashboard** menu -> **Actions** -> **Add Action** -> **Filter**.
2. **Action 1: Country Highlight**:
   - Source Sheet: `W1_Country_Medals`.
   - Run action on: **Select**.
   - Target Sheets: `W1_World_Map`, `W1_Year_Trend`.
   - Clearing the selection: **Show all values**.
3. **Action 2: Map Filter**:
   - Clicking a country on `W1_World_Map` filters all companion charts to that country's history!

---

## 🗣️ Step-by-Step Mentorship Walkthrough (Hinglish Guide)

Agar aap Tableau Public pehli baar use kar rahe hain, toh tension bilkul mat lijiye! Yeh 5 simple steps follow kijiye:

1. **Tableau Public Open Kijiye**:
   - App kholiye, left panel me **Text File** par click kijiye aur humara cleaned file `data/processed/medal_results.csv` select kijiye.
   - Tableau saare columns automatically load kar lega.

2. **Pehli Sheet (Top 15 Countries) Banayein**:
   - Bottom me "Sheet 1" tab par jaiye.
   - Left side (Data pane) se `country` ko uthakar **Rows** me drag kijiye.
   - `Measure Values` ko **Columns** me drag kijiye.
   - Filter shelf me jakar sirf `gold`, `silver`, `bronze` rakhiye.
   - `Measure Names` ko **Color** box par drop kijiye aur Gold ko Golden (`#D4AF37`), Silver ko Grey (`#A0AAB2`), Bronze ko Bronze (`#CD7F32`) color de dijiye.
   - Aapka beautiful stacked bar chart taiyyar!

3. **Year Trend Sheet Banayein**:
   - Nayi sheet lijiye (+ icon click karke).
   - `year` ko **Columns** me drop kijiye aur `athletes_count` ko **Rows** me drop kijiye.
   - `season` ko **Color** me drop kijiye. Dekhiye kaise Summer aur Winter Games ka historical growth do alag lines me dikhta hai!

4. **Host Nation Advantage Sheet**:
   - Data source me `host_nation_performance.csv` connect kijiye.
   - `country` aur `host_year` ko Columns me, aur `pre_medals`, `host_medals`, `post_medals` ko Rows me daliye.
   - Aapko saaf dikhega ki jab bhi koi country host banti hai, uske medals 86.7% cases me jump karte hain (Host Bounce effect)!

5. **Dashboard Assemble Karein**:
   - Bottom me **New Dashboard** icon par click kijiye.
   - Size ko `1366 x 768` set kijiye.
   - Saari sheets ko drag and drop karke clean boxes me arrange kijiye.
   - Top par Title likhiye: *"Global Olympic Sports Performance Analysis"*.
   - File -> **Save to Tableau Public As...** click karke submit kar dijiye!

