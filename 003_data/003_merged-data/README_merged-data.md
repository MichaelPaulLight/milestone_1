# Merged Data

This folder contains merged datasets resulting from the merge clean data scripts.

1. merged_cms_ballot-measures_by-assembly-district.parquet
    - This file contains data aggregated at the assembly district level across the CMS, CHHS, and SOS Ballot Data
    - For each year and assembly district, facility and patient care information can be found. This also includes how the assembly district voted in the proposition years and additional geographic values.
    - Created by 004_data-processing-scripts\003_merge-clean-data\merge_ballot-measures_cms-data.ipynb

2. merged_cms_ballot-measures_by-city.parquet
    - This file contains data aggregated at the city level across the CMS, CHHS, and SOS Ballot Data
    - For each year and city, facility and patient care information can be found. This also includes how the assembly district voted in the proposition years and additional geographic values.
    - Created by 004_data-processing-scripts\003_merge-clean-data\merge_ballot-measures_cms-data.ipynb