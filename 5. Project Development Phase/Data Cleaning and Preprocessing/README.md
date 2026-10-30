# Data Cleaning and Preprocessing: Pipeline Architecture & Transformations

**Project:** Global Olympic Sports Performance Analysis  
**Author:** Md. Firdous Alam  
**Live Dashboard:** [Tableau Public Profile](https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3)  

## Overview
Technical documentation of clean_data.py, covering imputation, filtering, team-event deduplication, and schema validation.

## Key Analytical Highlights
- Imputed missing country names via 230 NOC region crosswalk mappings
- Standardized medal column: ['Gold', 'Silver', 'Bronze', 'No Medal']
- Applied event-level deduplication to eliminate team-sport overcounting
- Engineered weighted scoring field: Weighted Score = 3*G + 2*S + 1*B

## Subfolder Assets & Artifacts
- `Data_Cleaning_and_Preprocessing.pdf`
