# System Architecture & Detailed Technical Design
## Global Olympic Sports Performance Analysis

---

## 1. High-Level Architecture Overview
The platform utilizes a decoupled, 3-tier data architecture ensuring clean separation between data storage, analytical processing, and business intelligence presentation.

```
[Raw Sources: IOC Archives & NOC Mappings]
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│               Data Engineering & Ingestion             │
│  - Type Coercion (clean_data.py)                       │
│  - Deterministic Event Deduplication                   │
│  - Storage Size Optimization (<25 MB)                  │
└────────────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│            Relational Datasets & Analytics             │
│  - athletes.csv (Modern Era, 157k rows, 22.78 MB)      │
│  - medal_results.csv (All 51 Editions, 3,837 rows)     │
│  - host_nation_performance.csv (15 Host Editions)      │
│  - sports_funding_benchmark.csv (UK Sport Grants)      │
└────────────────────────────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│  Tableau Public  │  │  Olympic-Flask   │
│  - Dashboard 1   │  │  - Web Portal    │
│  - Dashboard 2   │  │  - REST JSON API │
└──────────────────┘  └──────────────────┘
```

---

## 2. Component Design & Pipeline Execution

### Component A: Event Deduplication Algorithm
In team sports, multiple athletes share a single event victory. The deduplication algorithm groups by event attributes:
$$\text{Official\_Medals} = \text{UniqueCount}(\text{games\_id}, \text{noc}, \text{sport}, \text{event}, \text{medal})$$
This eliminates inflation bias and matches official IOC historical archival standards across 100% of editions.

### Component B: Moving-Average Host Benchmark
To evaluate the host nation performance surge:
$$\Delta \text{Medals} = \text{Medals}_{\text{Host}} - \text{Medals}_{\text{Pre-Games}}$$
$$\text{Surge Rate} = \frac{\text{Count}(\Delta \text{Medals} > 0)}{\text{Total Evaluated Hosts}} = \frac{13}{15} = 86.7\%$$
$$\text{Mean Bump} = \frac{\sum \Delta \text{Medals}}{15} = +15.4 \text{ medals}$$

### Component C: Sports Funding Econometric Model
Using audited UK Sport lottery disbursements:
$$r = \frac{\sum (X - \bar{X})(Y - \bar{Y})}{\sqrt{\sum (X - \bar{X})^2 \sum (Y - \bar{Y})^2}} = 0.752$$
$$\text{Cost Per Medal} = \frac{\text{Quadrennial Funding (£M)}}{\text{Medals Won}}$$

