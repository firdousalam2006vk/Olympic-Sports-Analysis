# Tableau Public Dashboard Guide: Global Olympic Performance Analysis

**Project**: Global Olympic Sports Performance Analysis  
**Target Environment**: Tableau Public (Desktop / Web Authoring)  
**Deliverable**: Complete Step-by-Step Construction Guide for 2 Professional Dashboards  

---

## 🎨 Professional Design System & Color Palette

To ensure an executive, publication-grade appearance:

| Element | Hex Code | Visual Application |
| :--- | :--- | :--- |
| **Primary Navy** | `#1B365D` | Headers, KPI bold values, primary series, frame borders |
| **Slate Blue** | `#2E6B9E` | Secondary lines, Winter Olympics series, interactive highlights |
| **Olympic Gold** | `#D4AF37` | Gold medals, benchmark lines, top performer callouts |
| **Olympic Silver** | `#A0AAB2` | Silver medal category |
| **Olympic Bronze**| `#CD7F32` | Bronze medal category |
| **Canvas Background** | `#F8FAFC` | Dashboard canvas and sheet background |
| **Card Background** | `#FFFFFF` | Individual KPI cards and container panels (Border: `#E2E8F0`) |
| **Dark Typography**| `#1E293B` | Titles, subtitles, axis labels |

---

## 🚀 Step 1: Connecting Data in Tableau Public

1. Launch **Tableau Public**.
2. Under **Connect -> To a File**, click **Text file**.
3. Select `data/medal_results.csv` from the project directory.
4. Verify field assignments in the Data Source pane:
   - `games_id`: String (e.g., `2016 Summer`)
   - `year`: Number (whole)
   - `country`: String -> Click data icon -> **Geographic Role** -> **Country/Region**
   - `gold`, `silver`, `bronze`, `total_medals`: Number (whole)
   - `is_host`: Number (whole)
   - `medals_per_100_athletes`: Number (decimal)

---

## 📐 Step 2: Creating Calculated Fields

In the left Data pane, click the down arrow next to the Search bar -> **Create Calculated Field**:

### 1. Weighted Medal Score
* **Name**: `CF_Weighted_Medal_Score`
* **Formula**:
  ```tableau
  ([gold] * 3) + ([silver] * 2) + ([bronze] * 1)
  ```

### 2. Medal Conversion Rate (%)
* **Name**: `CF_Medal_Conversion_Rate`
* **Formula**:
  ```tableau
  IF SUM([athletes_count]) > 0 THEN
      (SUM([total_medals]) / SUM([athletes_count])) * 100
  ELSE
      0
  END
  ```
* *Formatting*: Right-click field -> Default Properties -> Number Format -> Percentage (1 decimal place).

### 3. Host Status Display
* **Name**: `CF_Host_Status`
* **Formula**:
  ```tableau
  IF [is_host] = 1 THEN "Host Nation" ELSE "Visiting Competitor" END
  ```

---

## 📊 DASHBOARD 1: Global Olympic Performance

**Dimensions**: `1366 x 768 px` (Fixed Layout).  
**Goal**: Macro-level view of Olympic participation, nation standings, and historical growth.

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Global Olympic Performance Analysis | All-Time Historical Audit (1896-2016)              |
+---------------------------------------------------------------------------------------------------+
|  [KPI 1: 51 Editions]  |  [KPI 2: 135,571 Athletes]  |  [KPI 3: 18,905 Medals]  |  [KPI 4: 230 NOCs]  |
+-------------------------------------------------------------+-------------------------------------+
|  SHEET 1: All-Time Medal Table by Country (Top 15)          |  SHEET 2: Athlete Growth Trajectory |
|  (Horizontal Stacked Bar: Gold, Silver, Bronze)             |  (Dual-Line: Summer vs. Winter)     |
+-------------------------------------------------------------+-------------------------------------+
|  FILTERS: [Season: Summer/Winter] | [Year Slider: 1896-2016] | [Continent: All]                   |
+---------------------------------------------------------------------------------------------------+
```

### Sheet 1.1: KPI Cards (`W1_KPIs`)
1. Create a new sheet named `W1_KPIs`.
2. Drag `Measure Values` to **Text** on the Marks card.
3. Keep only:
   - `Distinct Count(games_id)` -> Alias: **Total Editions** (`51`)
   - `Sum(athletes_count)` -> Alias: **Athletes Entered** (`197k+` / `135,571` unique)
   - `Sum(total_medals)` -> Alias: **Official Medals** (`18,905`)
   - `Distinct Count(noc)` -> Alias: **Competing Nations** (`230`)
4. Font: `Arial Bold`, 20pt, Color `#1B365D`.

### Sheet 1.2: Country Medals Bar Chart (`W1_Country_Medals`)
1. Drag `country` to **Rows**.
2. Drag `Measure Values` to **Columns** (Keep `gold`, `silver`, `bronze`).
3. Drag `Measure Names` to **Color**:
   - `gold` -> `#D4AF37`
   - `silver` -> `#A0AAB2`
   - `bronze` -> `#CD7F32`
4. Sort `country` descending by `SUM(total_medals)`.
5. Filter `country` -> Top tab -> **Top 15** by `SUM(total_medals)`.

### Sheet 1.3: Longitudinal Growth Trend (`W1_Year_Trend`)
1. Drag `year` to **Columns**.
2. Drag `SUM(athletes_count)` to **Rows**.
3. Drag `season` to **Color** (Summer: Navy `#1B365D`, Winter: Slate Blue `#2E6B9E`).
4. Line thickness: 2.5pt. Mark labels on start/end peaks.

---

## 📊 DASHBOARD 2: Sports & Regional Efficiency

**Dimensions**: `1366 x 768 px` (Fixed Layout).  
**Goal**: Detailed comparative analysis of continental productivity, host advantage, and sport dominance.

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Sports & Regional Efficiency | Continental Benchmarks & Host Advantage                   |
+---------------------------------------------------------------------------------------------------+
|  SHEET 3: Continental Efficiency Analysis                   |  SHEET 4: The Host Nation Advantage |
|  (Bar: Medals per 100 Athletes by Continent)                |  (Pre vs. Host vs. Post Medals)     |
+-------------------------------------------------------------+-------------------------------------+
|  SHEET 5: Top 10 Sports by Medal Volume                     |  SHEET 6: Capital vs. Podium ROI    |
|  (Ranked Bar: Athletics, Swimming, Gymnastics, etc.)        |  (UK Sport Benchmark Scatter)       |
+---------------------------------------------------------------------------------------------------+
```

### Sheet 2.1: Continental Efficiency (`W2_Regional_Efficiency`)
1. Drag `continent` to **Columns**. Filter out `'Other'` and `'Special'`.
2. Drag `[CF_Medal_Conversion_Rate]` to **Rows**.
3. Show mark labels (Americas: `10.96%`, Europe: `10.94%`, Asia: `8.13%`, Oceania: `8.11%`, Africa: `4.00%`).
4. Color by `continent`.

### Sheet 2.2: Host Nation Advantage (`W2_Host_Advantage`)
1. Connect to `data/processed/host_nation_performance.csv`.
2. Drag `country` and `host_year` to **Columns**.
3. Drag `Measure Values` (`pre_medals`, `host_medals`, `post_medals`) to **Rows**.
4. Mark Type: Side-by-side bar. Colors: Pre (Silver), Host (Navy `#1B365D`), Post (Slate `#2E6B9E`).

### Sheet 2.3: Top Sports Dominance (`W2_Top_Sports`)
1. Connect to `data/athletes.csv`.
2. Filter `medal != 'No Medal'`.
3. Drag `sport` to Rows, sorted descending by `COUNT(event)` -> Top 10.
4. Drag `country` to Tooltip to reveal historical dominant powerhouses.

### Sheet 2.4: Capital Investment Benchmark (`W2_Investment_Scatter`)
1. Connect to `data/processed/sports_funding_benchmark.csv`.
2. Filter for `cycle = 'Rio 2016'`.
3. Drag `funding_millions_gbp` to **Columns**, `medals_won` to **Rows**.
4. Mark: Circle, Detail: `sport`, Trend line: Linear ($r = 0.752$).

---

## 🗣️ Step-by-Step Instructions in Simple Hinglish

Aapke pass already ek ready-made Tableau workbook maujood hai:  
`tableau/Olympic_Performance_Analysis.twb`.

Aapko bas yeh 4 steps follow karne hain:

1. **Tableau Public Kholiye**:
   - Tableau Public open karke **File -> Open** dabayein aur `tableau/Olympic_Performance_Analysis.twb` select kijiye.
   - Saara data aur basic sheets automatically load ho jayengi!
2. **Nayi Sheet Banayein**:
   - Agar aapko Regional Efficiency ya Host Advantage sheet add karni hai, toh bottom me **+** icon dabayein.
   - `continent` ko Columns me aur `medals_per_100_athletes` ko Rows me drop kijiye. 
3. **Professional Colors Set Kijiye**:
   - Gold ke liye `#D4AF37`, Silver ke liye `#A0AAB2`, aur Bronze ke liye `#CD7F32`.
   - Headers ko Deep Navy (`#1B365D`) color dijiye.
4. **Tableau Public Par Publish Kijiye**:
   - Top menu me **File -> Save to Tableau Public As...** click kijiye.
   - Apna Tableau Public login daliye aur workbook ka public link copy karke course submission form me paste kar dijiye!

