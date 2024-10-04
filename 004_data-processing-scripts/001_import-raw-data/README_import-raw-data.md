Notebooks included in this folder:

import-raw-data_cms_historical-facility-data.ipynb
    - This notebook downloads and processes Center for Medicare and Medicaid Services (CMS) data from 2017 to 2024 on dialysis facilities and their CAHPS scores.
    - It creates two parquet files:
        1. 2017-2024_national_cms_dialysis-facility_data.parquet
        2. 2017-2024_national_cms_dialysis-facility_cahps-data.parquet
    - Data manipulation steps taken:
        1. Generated URLs for CMS dialysis facility data zip files from 2017 to 2024.
        2. For each URL:
            a. Downloaded and extracted CSV files from zip archives.
            b. Standardized column names, including mapping provider column variations to 'provider_number'.
            c. Added 'year' and 'month' columns based on the data source.
            d. Concatenated facility and CAHPS data separately.
        3. Cast all columns to string type for consistency.
        4. Combined data from all years into single facility and CAHPS datasets.

import-raw-data_chhs_historical-facility-data.ipynb
    - This notebook downloads and processes California Health and Human Services (CHHS) data from 2013 to 2023 on dialysis facilities.
    - It creates one parquet file:
        1. 2013-2023_CHHS_dialysis-facility_data.parquet
    - Data manipulation steps taken:
        1. Standardized naming convention and data types for Census Tract and Facility Number columns.
        2. Created columns during import: 
            a. year column to identify the year of the data it pertains to.
            b. source_file column to identify the original file from which the data was obtained.
        3. Renamed columns in the pre-2018 dataframe to match the post-2018 dataframe using a data dictionary.
        4. Combined street address columns in the pre-2018 dataframe.
        5. Cleaned and converted specific columns to numeric types in the post-2018 dataframe.
        6. Converted acquisition-related columns in the pre-2018 dataframe to match the data types in the post-2018 dataframe.
        7. Dropped rows with missing FAC_NO in the merged dataframe.
        8. Converted columns with mixed types to string and numeric columns to float in the merged dataframe.

import-raw-data_sos_ballot-measure-votes.ipynb
    - This notebook downloads and processes sub-county level data (city, district, census tract, etc.) on ballot measures from 2018 to 2022 in California.
    - It creates one parquet file:
        1. 2018-2022_ballot-measure_sub-county_data.parquet
    - Data manipulation steps taken:
        1. Downloaded Excel files from California Secretary of State website for 2018, 2020, and 2022 elections.
        2. Processed each Excel file:
            a. Selected first two columns (county and sub_county).
            b. Identified and selected columns related to kidney/dialysis propositions and their corresponding No vote columns.
            c. Renamed columns: first two as 'county' and 'sub_county', proposition column as 'yes', following column as 'no'.
            d. Added 'year' column to each dataset.
        3. Combined data from all years into a single DataFrame.
        4. Unnested sub-county data into geo_type and sub_county_id.
        5. Reshaped data:
            a. Unpivoted 'yes' and 'no' columns.
            b. Renamed columns to make them easier to interpret :
                i. yes/no vote column as 'vote_type'
                ii. sub_county_id as 'district_id'
        7. Reordered columns for clarity/readability