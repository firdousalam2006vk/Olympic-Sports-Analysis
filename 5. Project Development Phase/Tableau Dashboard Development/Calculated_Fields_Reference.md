# Tableau Calculated Fields Reference Guide

This reference provides exact, copy-paste formulas for all calculated fields, parameters, and Level of Detail (LOD) expressions required for the Olympic Dashboards in Tableau Public.

---

## 1. Core Performance Metrics (`medal_results.csv`)

### 1.1 Weighted Medal Score
* **Field Name**: `[CF_Weighted_Medal_Score]`
* **Formula**:
  ```tableau
  ([Gold] * 3) + ([Silver] * 2) + ([Bronze] * 1)
  ```
* **Purpose**: Provides a standardized valuation honoring podium quality (Gold=3, Silver=2, Bronze=1).

### 1.2 Medal Conversion Efficiency (%)
* **Field Name**: `[CF_Medal_Conversion_Rate]`
* **Formula**:
  ```tableau
  IF SUM([Athletes Count]) > 0 THEN
      (SUM([Total Medals]) / SUM([Athletes Count])) * 100
  ELSE
      0
  END
  ```
* **Default Number Formatting**: Number (Custom) -> 2 decimal places, Suffix: `%`.

### 1.3 Gold Medal Quality Ratio
* **Field Name**: `[CF_Gold_Share_Pct]`
* **Formula**:
  ```tableau
  IF SUM([Total Medals]) > 0 THEN
      SUM([Gold]) / SUM([Total Medals])
  ELSE
      0
  END
  ```
* **Default Number Formatting**: Percentage -> 1 decimal place.

### 1.4 Host Nation Display Status
* **Field Name**: `[CF_Host_Status_Label]`
* **Formula**:
  ```tableau
  IF [Is Host] = 1 THEN 
      "Host Nation" 
  ELSE 
      "Visiting Competitor" 
  END
  ```

---

## 2. Dashboard KPI Card Calculations

### 2.1 Total Olympic Editions
* **Field Name**: `[KPI_Total_Editions]`
* **Formula**:
  ```tableau
  COUNTD([Games Id])
  ```

### 2.2 Total Participating Athletes
* **Field Name**: `[KPI_Total_Athletes]`
* **Formula**:
  ```tableau
  SUM([Athletes Count])
  ```
  *(Or `COUNTD([Athlete Id])` when using `athletes.csv`)*

### 2.3 Total Official Medals
* **Field Name**: `[KPI_Total_Medals]`
* **Formula**:
  ```tableau
  SUM([Total Medals])
  ```

### 2.4 Total Competing Nations
* **Field Name**: `[KPI_Total_Nations]`
* **Formula**:
  ```tableau
  COUNTD([Noc])
  ```

---

## 3. Host Nation Advantage Analysis (`host_nation_performance.csv`)

### 3.1 Host Net Medal Surge
* **Field Name**: `[CF_Host_Medal_Bump]`
* **Formula**:
  ```tableau
  ZN([Host Medals]) - ZN([Pre Medals])
  ```

### 3.2 Host Growth Percentage
* **Field Name**: `[CF_Host_Growth_Pct]`
* **Formula**:
  ```tableau
  IF ZN([Pre Medals]) > 0 THEN
      (([Host Medals] - [Pre Medals]) / [Pre Medals]) * 100
  ELSE
      NULL
  END
  ```

### 3.3 Host Advantage Classification
* **Field Name**: `[CF_Host_Impact_Tier]`
* **Formula**:
  ```tableau
  IF [CF_Host_Growth_Pct] >= 50 THEN
      "Exceptional Surge (>= 50%)"
  ELSEIF [CF_Host_Growth_Pct] > 0 THEN
      "Positive Host Bump (0 - 50%)"
  ELSEIF [CF_Host_Growth_Pct] = 0 THEN
      "Neutral Performance"
  ELSE
      "Underperformed Post-Host"
  END
  ```

---

## 4. Investment & Capital ROI Analysis (`sports_funding_benchmark.csv`)

### 4.1 Cost Per Medal (£ Millions)
* **Field Name**: `[CF_Cost_Per_Medal]`
* **Formula**:
  ```tableau
  IF SUM([Medals Won]) > 0 THEN
      SUM([Funding Millions Gbp]) / SUM([Medals Won])
  ELSE
      NULL
  END
  ```

### 4.2 Investment Efficiency Tier
* **Field Name**: `[CF_Investment_Efficiency_Tier]`
* **Formula**:
  ```tableau
  IF [Cost Per Medal Millions Gbp] < 3.0 THEN
      "Tier 1: High Efficiency (< £3.0M / Medal)"
  ELSEIF [Cost Per Medal Millions Gbp] <= 7.0 THEN
      "Tier 2: Moderate Efficiency (£3.0M - £7.0M)"
  ELSEIF [Cost Per Medal Millions Gbp] > 7.0 THEN
      "Tier 3: Capital Intensive (> £7.0M / Medal)"
  ELSE
      "No Podium Return"
  END
  ```

---

## 5. Level of Detail (LOD) Expressions for Benchmarking

### 5.1 Global Average Medals per Nation (Fixed by Games)
* **Formula**:
  ```tableau
  { FIXED [Games Id] : AVG({ FIXED [Games Id], [Noc] : SUM([Total Medals]) }) }
  ```

### 5.2 Country All-Time Peak Medals
* **Formula**:
  ```tableau
  { FIXED [Noc] : MAX([Total Medals]) }
  ```

### 5.3 Relative Performance Index (RPI)
* **Formula**:
  ```tableau
  SUM([Total Medals]) / { FIXED [Games Id] : MAX([Total Medals]) }
  ```

