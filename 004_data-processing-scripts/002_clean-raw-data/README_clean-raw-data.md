This folder contains the following notebooks:

national_cms_dialysis-facility_cleaning.ipynb
    - This notebook cleans and processes the CMS dialysis facility data.
    - Key operations:
        1. Loads and filters data for California from two source files:
           - 2017-2024_national_cms_dialysis-facility_data.parquet
           - 2017-2024_national_cms_dialysis-facility_cahps-data.parquet
        2. Merges duplicate columns and standardizes column names
        3. Cleans and standardizes categorical variables
        4. Removes redundant columns
        5. Standardizes values (e.g., converting Y/N to yes/no)
        6. Processes provider numbers to remove leading zeros
        7. Selects relevant columns for the final datasets
    - Outputs two cleaned parquet files:
        - national_cms_dialysis-facility_data.parquet
        - national_cms_dialysis-facility_cahps-data.parquet
    - Adds metadata to the output files including creation timestamp, 
      description, version, and cleaning steps performed

The cleaned data files are saved in the '../../003_data/002_clean-data/' directory. They are used subsequently in ../003_merge-clean-data/merge_ballot-measures_cms-data.ipynb
