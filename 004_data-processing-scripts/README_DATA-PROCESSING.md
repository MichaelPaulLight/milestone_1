This folder contains all the scripts/notebooks used to process data.

Folders include
    - 001_import-raw-data: 
        includes 3 notebooks which download data from each one of the sources ,CMS, CHHS, and SOS Ballot data, from their url. these notebooks include some initial cleaning and manipulation in order to aggregate the data files over our years of interest. raw data in saved into the 003_data/001_raw-data folder.

    - 002_clean-raw-data:
        includes 2 notebooks which clean the CMS and CHHS data sets using the raw data from the 003_data/001_raw-data folder. the cleaned data is stored in the 003_data/002_clean-data folder.

    - 003_merge-clean data:
        includes 1 notebook which aggregates the clean data from the 003_data/002_clean-data folder into 2 files. one which aggregates all data (CMS, CHHS, and SOS) at the assembly district level and one which aggregates all data to the city level. the notebook creates 2 files saved in the 003_data/003_merged-data folder.