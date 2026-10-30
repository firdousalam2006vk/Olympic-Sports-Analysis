# Data Flow Diagrams (DFD) & UML Specifications
## Global Olympic Sports Performance Analysis

---

## 1. DFD Level 0 (Context Diagram)

```
                       ┌─────────────────────────┐
                       │  IOC Historical Source  │
                       └─────────────────────────┘
                                    │
                                    │ Raw Competition Records
                                    ▼
┌──────────────┐       ┌─────────────────────────┐       ┌──────────────────┐
│              │       │                         │       │                  │
│ Public /     │ <───> │  Olympic Analytics      │ <───> │ Sports Ministry  │
│ Researcher   │       │  Platform Pipeline      │       │ Analysts         │
│              │       │                         │       │                  │
└──────────────┘       └─────────────────────────┘       └──────────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │  Tableau Public Cloud   │
                       └─────────────────────────┘
```

---

## 2. DFD Level 1 (Decomposition Diagram)

```mermaid
graph TD
    A[Raw Olympic CSV] --> B(1.0 Ingest & Type Coerce)
    B --> C{2.0 Team Event?}
    C -- Yes --> D(Collapse Multi-Player Rows)
    C -- No --> E(Retain Individual Record)
    D --> F[Deterministic Deduplicated Medals]
    E --> F
    F --> G(3.0 Aggregate Country Standings)
    F --> H(4.0 Compute Host Advantage Bump)
    F --> I(5.0 Model High-Performance ROI)
    G --> J[medal_results.csv]
    H --> K[host_nation_performance.csv]
    I --> L[sports_funding_benchmark.csv]
    J --> M[Tableau Public Dashboards]
    J --> N[Olympic-Flask Web Portal]
```

---

## 3. UML Use Case Diagram

```mermaid
graph LR
    User((Data Analyst))
    Gov((Sports Ministry))

    User --> UC1[View Macro Leaderboard]
    User --> UC2[Filter by Season & Year]
    User --> UC3[Inspect Athlete Biometrics]
    
    Gov --> UC4[Evaluate Host Advantage]
    Gov --> UC5[Assess High-Performance Funding ROI]
    Gov --> UC6[Export Quality-Checked Data]
```

