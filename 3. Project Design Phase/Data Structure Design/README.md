# Data Structure Design: Entity Relational Schema & Data Dictionaries

**Project:** Global Olympic Sports Performance Analysis  
**Author:** Md. Firdous Alam  
**Live Dashboard:** [Tableau Public Profile](https://public.tableau.com/app/profile/md.firdous.alam/viz/GlobalOlympicSportsPerformanceAnalysis_17933559199720/Dashboard3)  

## Overview
Entity-Relationship model and complete data dictionary specifying types, nullability, constraints, and descriptions for all tables.

## Key Analytical Highlights
- Athletes Entity: 18 attributes (id, name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal, medal_value, is_medal, country)
- Medal Results Entity: 11 attributes (games_id, year, season, city, noc, country, gold, silver, bronze, total_medals, weighted_score)
- Primary Keys: [id, games, event] for athletes; composite [games_id, noc] for medal results

## Subfolder Assets & Artifacts
- `Data_Structure_Design.pdf`
