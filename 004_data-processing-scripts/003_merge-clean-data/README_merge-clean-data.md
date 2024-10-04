# Merge Ballot Measures and CMS Data

This folder contains the following notebook:

## merge_ballot-measures_cms-data.ipynb
This notebook merges cleaned CMS dialysis facility data with ballot measure data and supplemental facility information.

Key operations:
1. Loads cleaned data:
   - CMS dialysis facility data
   - CMS CAHPS data
   - Ballot measure data
   - Supplemental facility data from CHHS
2. Merges CMS facility and CAHPS data
3. Standardizes data:
   - Converts year columns to string type
   - Lowercases county and city names
   - Standardizes facility and chain organization names
4. Performs data validation on county names across datasets
5. Filters supplemental facility data to include only chronic dialysis clinics
6. Merges CMS data with supplemental facility data using standardized facility names and zip codes
7. Reshapes ballot measures data for city-level and assembly-district-level analysis
8. Creates two final datasets:
   - City-level analysis: Merges CMS data with city-level ballot measure data
   - Assembly-district-level analysis: Merges supplemented CMS data with assembly-district-level ballot measure data
9. Selects variables of interest for each analysis type
10. Saves the final merged datasets as parquet files with metadata:
    - merged_cms_ballot-measures_by-city.parquet
    - merged_cms_ballot-measures_by-assembly-district.parquet

The merged data files are saved in the '../../003_data/003_merged-data/' directory. They are used subsequently in analysis/modeling notebooks.
