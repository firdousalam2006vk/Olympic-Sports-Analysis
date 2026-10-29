# Tableau Data Dictionary: Global Olympic Sports Performance Analysis

This document details the schema, data types, primary keys, and field definitions for the datasets used in Tableau Public dashboards.

---

## 1. Primary Dataset: `medal_results.csv`
**Granularity**: One record per Country (`noc`) per Olympic Games Edition (`games_id`).  
**Row Count**: 3,861 rows.  
**Primary Key**: Composite key `[games_id, noc]`.

| Field Name | Data Type | Role | Sample Value | Description & Business Definition |
| :--- | :--- | :--- | :--- | :--- |
| `games_id` | String | Dimension | `2016 Summer` | Unique Games identifier combining Year and Season. |
| `year` | Integer | Dimension / Date | `2016` | Calendar year the Olympic Games took place. |
| `season` | String | Dimension | `Summer` | Olympic Season (`Summer` or `Winter`). |
| `city` | String | Dimension | `Rio de Janeiro` | Host city where the Games were celebrated. |
| `noc` | String | Dimension | `USA` | National Olympic Committee 3-letter IOC country code. |
| `country` | String | Dimension (Geo) | `United States` | Standardized national name for mapping & reporting. |
| `continent` | String | Dimension | `Americas` | Global Olympic Continental Association (`Europe`, `Americas`, `Asia`, `Oceania`, `Africa`). |
| `is_host` | Integer / Boolean | Dimension | `0` or `1` | Flag: `1` if this nation was the host of this edition, `0` otherwise. |
| `athletes_count`| Integer | Measure (Sum) | `555` | Total unique athletes representing this NOC at these Games. |
| `events_entered`| Integer | Measure (Sum) | `245` | Total distinct sports events contested by this nation's athletes. |
| `sports_entered`| Integer | Measure (Sum) | `33` | Total distinct Olympic disciplines entered by this nation. |
| `gold` | Integer | Measure (Sum) | `46` | Official deduplicated Gold medals won by this country. |
| `silver` | Integer | Measure (Sum) | `37` | Official deduplicated Silver medals won by this country. |
| `bronze` | Integer | Measure (Sum) | `38` | Official deduplicated Bronze medals won by this country. |
| `total_medals` | Integer | Measure (Sum) | `121` | Total official podium finishes (`gold + silver + bronze`). |
| `weighted_score`| Integer | Measure (Sum) | `250` | Weighted medal index: `(Gold * 3) + (Silver * 2) + (Bronze * 1)`. |
| `medals_per_100_athletes` | Float | Measure (Avg) | `21.80` | Athlete Conversion Efficiency: `(total_medals / athletes_count) * 100`. |

---

## 2. Granular Athlete Dataset: `athletes.csv`
**Granularity**: One record per Athlete per Event Participation.  
**Row Count**: 271,116 rows.  
**Primary Key**: Composite key `[athlete_id, games, event]`.

| Field Name | Data Type | Role | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| `athlete_id` | Integer | Dimension | `1` | Unique athlete identifier. |
| `name` | String | Dimension | `Michael Fred Phelps, II` | Full registered name of the Olympian. |
| `sex` | String | Dimension | `M` or `F` | Gender of the athlete. |
| `age` | Float / Int | Measure / Dim | `23` | Age of athlete at the time of competition. |
| `age_group` | String | Dimension | `20-24` | Categorical binned age bracket (`Under 20`, `20-24`, `25-29`, `30-34`, `35+`). |
| `height_cm` | Float | Measure (Avg) | `193.0` | Athlete height in centimeters (where recorded). |
| `weight_kg` | Float | Measure (Avg) | `88.0` | Athlete weight in kilograms (where recorded). |
| `team` | String | Dimension | `United States` | Competing team designation. |
| `noc` | String | Dimension | `USA` | 3-letter National Olympic Committee code. |
| `country` | String | Dimension (Geo) | `United States` | Standardized country name. |
| `continent` | String | Dimension | `Americas` | Continental region. |
| `games` | String | Dimension | `2008 Summer` | Full Games title. |
| `year` | Integer | Dimension | `2008` | Year of competition. |
| `season` | String | Dimension | `Summer` | Season (`Summer` / `Winter`). |
| `city` | String | Dimension | `Beijing` | Host city. |
| `sport` | String | Dimension | `Swimming` | Olympic sport discipline. |
| `event` | String | Dimension | `Swimming Men's 200 metres Butterfly` | Specific competitive event. |
| `medal` | String | Dimension | `Gold` | Athlete medal result (`Gold`, `Silver`, `Bronze`, `No Medal`). |
| `is_medalist` | Integer / Boolean | Measure / Dim | `1` | Binary flag: `1` if podium finisher, `0` otherwise. |
| `is_host` | Integer / Boolean | Dimension | `0` | Binary indicator for home nation status. |

---

## 3. Host Advantage Dataset: `host_nation_performance.csv`
**Granularity**: One record per Modern Summer Host Nation edition (1952-2016).  
**Row Count**: 17 rows.  
**Primary Key**: `[host_year, noc]`.

| Field Name | Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `host_year` | Integer | Dimension | Year the country hosted the Olympic Games. |
| `host_city` | String | Dimension | Host city name. |
| `country` | String | Dimension | Host nation name. |
| `pre_medals` | Float | Measure | Total medals won in previous edition ($t-1$). |
| `host_medals`| Float | Measure | Total medals won during host edition ($t=0$). |
| `post_medals`| Float | Measure | Total medals won in following edition ($t+1$). |
| `medal_bump` | Float | Measure | Absolute net change: `host_medals - pre_medals`. |
| `medal_bump_pct` | Float | Measure | Percentage surge: `(medal_bump / pre_medals) * 100`. |

---

## 4. Benchmark Investment Dataset: `sports_funding_benchmark.csv`
**Granularity**: One record per Olympic Sport per UK Sport Olympic High Performance Funding Cycle.  
**Row Count**: 36 rows.  
**Primary Key**: `[cycle, sport]`.  
**Data Integrity Notice**: Authentic, published public funding records from UK Sport High Performance Strategy (London 2012 & Rio 2016 cycles).

| Field Name | Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `sport` | String | Dimension | High-performance Olympic discipline. |
| `cycle` | String | Dimension | 4-year Olympic quadrennial cycle (`Rio 2016`, `London 2012`). |
| `games_year`| Integer | Dimension | Olympic Games year. |
| `funding_millions_gbp` | Float | Measure | Total National Lottery & Exchequer grant funding (£ Millions). |
| `medals_won`| Integer | Measure | Total Olympic medals won by Team GB in that sport. |
| `cost_per_medal_millions_gbp` | Float | Measure | Capital efficiency: `funding_millions_gbp / medals_won`. |
| `target_met`| String | Dimension | UK Sport performance target achievement (`Yes` / `No`). |
| `data_source` | String | Dimension | Official audit attribution string. |

---

## 5. Tableau Relationship Model (Recommended Data Source Setup)

In Tableau Public:
1. Connect to **Text File** -> select `data/processed/medal_results.csv` as the root table.
2. Drag `data/processed/host_nation_performance.csv` and relate on:
   - `medal_results.year` = `host_nation_performance.host_year`
   - `medal_results.noc` = `host_nation_performance.noc`
3. Drag `data/processed/sports_funding_benchmark.csv` as an independent data source or connect for sport-level scatter visualization.

