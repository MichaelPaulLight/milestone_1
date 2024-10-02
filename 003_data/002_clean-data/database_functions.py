from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import os
import re

def generate_file_names(directory_path=None):
    """
    Input: path to the directory containing the cleaned CSV files
    output: dictionary of {table_name: file_name}
    """
    # default to current directory
    if directory_path is None:
        directory_path = os.path.dirname(os.path.abspath(__file__)) 
    
    file_names = {}
    for file in os.listdir(directory_path):
        if file.upper().endswith('CLEANED.CSV'):
            # Remove '_CLEANED.csv' and convert to lowercase
            table_name = re.sub(r'_?CLEANED\.CSV$', '', file, flags=re.IGNORECASE).lower() 
            file_names[table_name] = file

    return file_names

def generate_column_name_mappings(column_names_dict):
    def clean_column_name(name):
        """Cleans and standardizes a column name."""
        name = name.lower()
        name = re.sub(r'[^\w\s]', '_', name)
        name = re.sub(r'\s+', '_', name)
        name = re.sub(r'_+', '_', name)
        return name.strip('_')

    def get_unique_name(name, used_names):
        """Checks if column name is unique and appends a number if not unique."""
        base_name = name
        counter = 1
        while name in used_names:
            name = f"{base_name}_{counter}"
            counter += 1
        return name

    column_name_mapping = {}
    all_used_names = set()

    for table_name, columns in column_names_dict.items():
        table_mapping = {}
        used_names = set()

        for col in columns:
            cleaned_name = clean_column_name(col)
            if cleaned_name == 'unnamed_0':
                cleaned_name = 'id'
            elif cleaned_name in ['county_name', 'county']:
                cleaned_name = 'county_name'
            elif cleaned_name in ['year']:
                cleaned_name = 'year'
            else:
                # Handle special cases like percentages and years
                cleaned_name = re.sub(r'(\d+)_years_and_over', r'age_\1_plus', cleaned_name)
                cleaned_name = re.sub(r'(\d+)_to_(\d+)_years', r'age_\1_\2', cleaned_name)
                cleaned_name = re.sub(r'_?%\.?\d*$', '_percentage', cleaned_name)
                cleaned_name = re.sub(r'^(\d{4})$', r'year_\1', cleaned_name)
                cleaned_name  = get_unique_name(cleaned_name, used_names.union(all_used_names))

            table_mapping[col] = cleaned_name 
            if cleaned_name not in ['county_name', 'year']:  # Don't add 'county_name' to used_names
                used_names.add(cleaned_name)
                all_used_names.add(cleaned_name)
                
        column_name_mapping[table_name] = table_mapping

    return column_name_mapping

def read_dataframes(base_path=None):
    
    if base_path is None:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    file_names = generate_file_names(base_path)
    
    # Read column names from CSV files
    column_names_dict = {table_name: pd.read_csv(os.path.join(base_path, file_name), nrows=0).columns.tolist() 
                         for table_name, file_name in file_names.items()}
    
    # Generate column name mappings
    column_name_mapping = generate_column_name_mappings(column_names_dict)
    
    dataframes = {}
    
    for table_name, file_name in file_names.items():
        df = pd.read_csv(os.path.join(base_path, file_name))
        df.rename(columns=column_name_mapping[table_name], inplace=True)
        if 'id' in df.columns:
            df.drop(columns=['id'], inplace=True)
        df['county_name'] = df['county_name'].str.strip()
        dataframes[table_name] = df
            
    
    # if 'demo' in dataframes and 'demo_add' in dataframes:
    #     dataframes['demo'] = pd.merge(dataframes['demo'], dataframes['demo_add'], on='county_name', how='right')
    #     dataframes.pop('demo_add')
    
    return dataframes

class Table:
    def __init__(self, df: pd.DataFrame, views: Dict[str, List[str]], database: 'Database', table_name: str):
        self._df = df
        self._df = df
        self._views = views
        self._database = database
        self._table_name = table_name
        self.columns = self.get_columns()

    def __getattr__(self, view_name: str) -> pd.DataFrame:
        """Get a view of the table by attribute access."""
        clean_view_name = view_name[1:] if view_name.startswith('_') else view_name
        if clean_view_name in self._views:
            return self._df[self._views[clean_view_name]]
        raise ValueError(f"View '{view_name}' not found")

    def __call__(self) -> pd.DataFrame:
        """Return the full dataframe when the table is called."""
        return self._df
    
    def list_views(self) -> List[str]:
        """Return a list of available views."""
        return list(self._views.keys())
    
    def add_view(self, view_name: str, columns: List[str]) -> None:
        """Add a new view to the table and update the database."""
        self._views[view_name] = columns
        self._database.update_view(self._table_name, view_name, columns)


    def get_view(self, view_name: str) -> pd.DataFrame:
        """Get a view of the table by name."""
        if view_name in self._views:
            return self._df[self._views[view_name]]
        raise ValueError(f"View '{view_name}' not found")
    
    def get_columns(self) -> List[str]:
        """Return a list of column names in the table."""
        return list(self._df.columns)

class Database:
    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = read_dataframes()
        self.views: Dict[str, Dict[str, List[str]]] = self.create_views()
        self.tables: Dict[str, Table] = {}
        for table_name, df in self.dataframes.items():
            self.tables[table_name] = Table(df, self.views.get(table_name, {}), self, table_name)
            setattr(self, table_name, self.tables[table_name])
        self.merged: Optional[pd.DataFrame] = None

    def create_views(self) -> Dict[str, Dict[str, List[str]]]:
        """Create predefined views for each table."""
        views = {
            'ballot': {
                '2018': ['county_name', 'yes_count_2018', 'no_count_2018', 'total_count_2018', 'yes_perc_2018', 'no_perc_2018'],
                '2020': ['county_name', 'yes_count_2020', 'no_count_2020', 'total_count_2020', 'yes_perc_2020', 'no_perc_2020'],
                '2022': ['county_name', 'yes_count_2022', 'no_count_2022', 'total_count_2022', 'yes_perc_2022', 'no_perc_2022'],
                'all_counts': ['county_name', 'yes_count_2020', 'no_count_2020', 'total_count_2020', 'yes_count_2018', 'no_count_2018', 'total_count_2018', 'yes_count_2022', 'no_count_2022', 'total_count_2022'],
                'all_percentages': ['county_name', 'yes_perc_2020', 'no_perc_2020', 'yes_perc_2018', 'no_perc_2018', 'yes_perc_2022', 'no_perc_2022'],
            },
            'demo': {
                'population': ['county_name', 'population_january_2023', 'median_household_income_2021'],
                'race_ethnicity': ['county_name', 'one_race', 'some_other_race', 'two_or_more_races', 'total_races_tallied', 
                                'white_alone_or_in_combination_with_one_or_more_other_races', 'black_or_african_american_alone_or_in_combination_with_one_or_more_other_races', 
                                'american_indian_and_alaska_native_alone_or_in_combination_with_one_or_more_other_races', 
                                'asian_alone_or_in_combination_with_one_or_more_other_races', 
                                'native_hawaiian_and_other_pacific_islander_alone_or_in_combination_with_one_or_more_other_races', 
                                'hispanic_or_latino_of_any_race', 'race_ethnicity_american_indian_2023', 
                                'race_ethnicity_asian_2023', 'race_ethnicity_black_2023', 'race_ethnicity_hispanic_2023', 
                                'race_ethnicity_multi_racial_ethnic_2023', 'race_ethnicity_hawaiian_pacific_island_2023', 
                                'race_ethnicity_white_2023'],
                'age_groups': ['county_name', 'age_0_5_2023', 'age_6_17_2023', 'age_18_64_2023', 'age_65_2023'],
                'age_distribution': ['county_name', 'under_5_years', 'age_5_9', 'age_10_14', 
                                    'age_15_19', 'age_20_24', 'age_25_29', 
                                    'age_30_34', 'age_35_39', 'age_40_44', 
                                    'age_45_49', 'age_50_54', 'age_55_59', 
                                    'age_60_64', 'age_65_69', 'age_70_74', 
                                    'age_75_79', 'age_80_84', 'age_85_plus', 
                                    'age_16_plus', 'age_18_plus', 'age_21_plus', 
                                    'age_62_plus', 'age_65_plus'],
                'gender_distribution': ['county_name', 'male_population', 'female_population'],
                'household_composition': ['county_name', 'in_households', 'householder', 'total_households', 
                                        'married_couple_household', 'cohabiting_couple_household', 
                                        'male_householder_no_spouse_or_partner_present', 'female_householder_no_spouse_or_partner_present', 
                                        'households_with_individuals_under_18_years', 
                                        'households_with_individuals_age_65_plus', 'median_household_income_2021']
            },
            'fascility': {
                'summary': ['year', 'county_name', 'fac_count', 'stations', 'prof_np', 'chain_own'],
                'ratings': ['year', 'county_name', 'fac_star', 'xp_star', 'comm_scr', 'quality_scr', 'info_scr', 'phys_scr', 'staff_scr', 'fac_scr']
            },
            'medicare': {
                'payments': ['year_1', 'county_name', 'pymt_amt', 'pymt_pct', 'pymt_pc', 'pymt_per_user', 'stdz_pymt_amt', 'stdz_pymt_pct', 'stdz_pymt_pc', 'stdz_pymt_per_user'],
                'standardized_payments': ['year_1', 'county_name', 'stdz_pymt_amt', 'stdz_pymt_pct', 'stdz_pymt_pc', 'stdz_pymt_per_user'],
                'visits': ['year_1', 'county_name', 'user_cnt', 'user_pct', 'visits_per_1000']
            },
            'voter': {
                '2018': ['county_name', 'eligible_2018', 'total_registered_2018', 'democratic_2018', 'republican_2018', 'american_independent_2018', 'green_2018', 
                        'libertarian_2018', 'peace_and_freedom_2018', 'unknown_2018', 'other_2018', 'no_party_preference_2018'],
                '2020': ['county_name', 'eligible_2020', 'total_registered_2020', 'democratic_2020', 'republican_2020', 'american_independent_2020', 'green_2020', 
                        'libertarian_2020', 'peace_and_freedom_2020', 'unknown_2020', 'other_2020', 'no_party_preference_2020'],
                '2022': ['county_name', 'eligible_2022', 'total_registered_2022', 'democratic_2022', 'republican_2022', 'american_independent_2022', 'green_2022', 
                        'libertarian_2022', 'peace_and_freedom_2022', 'unknown_2022', 'other_2022', 'no_party_preference_2022']
            }
        }
        return views

    def update_view(self, table_name: str, view_name: str, columns: List[str]) -> None:
        """Update the database's view dictionary when a table's view is added or modified."""
        if table_name not in self.views:
            self.views[table_name] = {}
        self.views[table_name][view_name] = columns

    def add_view(self, table_name: str, view_name: str, columns: List[str]) -> None:
        """Add a new view to a specific table and update the database's view dictionary."""
        if table_name in self.tables:
            self.tables[table_name].add_view(view_name, columns)
        else:
            raise ValueError(f"Table '{table_name}' not found")
    
    def get_view(self, table_name: str, view_name: str) -> pd.DataFrame:
        """Get a view from a specific table."""
        if table_name in self.tables:
            return self.tables[table_name].get_view(view_name)
        else:
            raise ValueError(f"Table '{table_name}' not found")
        
    def merge_views(self, views_list: List[Tuple[str, str]]) -> pd.DataFrame:
        """Concatenate multiple views from different tables."""
        dfs_to_concat = [self.get_view(table_name, view_name) for table_name, view_name in views_list]
        concatenated_df = pd.concat(dfs_to_concat, ignore_index=True)
        
        # Move 'county_name' and 'year' to the front if they exist
        cols_to_front = ['county_name', 'year']
        for col in reversed(cols_to_front):
            if col in concatenated_df.columns:
                concatenated_df.insert(0, col, concatenated_df.pop(col))
        return concatenated_df

    def merge_all(self) -> pd.DataFrame:
        """Concatenate all tables into a single dataframe."""
        dfs_to_concat = [df for df in self.dataframes.values()]
        concatenated_df = pd.concat(dfs_to_concat, ignore_index=True)
        
        # Move 'county_name' and 'year' to the front if they exist
        cols_to_front = ['county_name', 'year']
        for col in reversed(cols_to_front):
            if col in concatenated_df.columns:
                concatenated_df.insert(0, col, concatenated_df.pop(col))
        return concatenated_df

    def query(self, conditions: Dict[str, Any], columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Query the merged dataset based on conditions.
        
        :param conditions: A dictionary of column-value pairs to filter on
        :param columns: Optional list of columns to return
        :return: Filtered DataFrame
        """
        result = self.merge_all()
        for column, value in conditions.items():
            if callable(value):
                result = result[value(result[column])]
            else:
                result = result[result[column] == value]
        
        if columns:
            result = result[columns]
        
        return result