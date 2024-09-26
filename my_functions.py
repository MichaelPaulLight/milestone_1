from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import os
import re

def read_dataframes():
    # Clean data folder and file names
    base_path = r'003_data\002_clean-data' 
    file_names = {  # table_name: file_name
        'ballot': 'BALLOT_CLEANED.csv',
        'demo': 'DEMO_CLEANED.csv',
        'demo_add': 'DEMO_ADD_CLEANED.csv',
        'facility': 'FASCILITY_CLEANED.csv',
        'medicare': 'MEDICARE_CLEAN.csv',
        'voter': 'VOTER_REG_CEANED.csv'
    }
    
    # Target column names for each dataframe
    column_name_mapping = { # table_name: [column_names]
        'ballot': [
            'id', 'county_name', 'yes_count_2020', 'no_count_2020', 'total_count_2020', 'yes_percentage_2020', 'no_percentage_2020',
            'yes_count_2018', 'no_count_2018', 'total_count_2018', 'yes_percentage_2018', 'no_percentage_2018',
            'yes_count_2022', 'no_count_2022', 'total_count_2022', 'yes_percentage_2022', 'no_percentage_2022'
        ],
        'demo': [
            'county_name', 'under_5_years_percentage', '5_to_9_years_percentage', '10_to_14_years_percentage', 
            '15_to_19_years_percentage', '20_to_24_years_percentage', '25_to_29_years_percentage', 
            '30_to_34_years_percentage', '35_to_39_years_percentage', '40_to_44_years_percentage', 
            '45_to_49_years_percentage', '50_to_54_years_percentage', '55_to_59_years_percentage', 
            '60_to_64_years_percentage', '65_to_69_years_percentage', '70_to_74_years_percentage', 
            '75_to_79_years_percentage', '80_to_84_years_percentage', '85_and_over_percentage', 
            '16_and_over_percentage', '18_and_over_percentage', '21_and_over_percentage', '62_and_over_percentage', 
            '65_and_over_percentage', 'male_population_percentage', 'under_5_years_percentage_1', 
            '5_to_9_years_percentage_1', '10_to_14_years_percentage_1', '15_to_19_years_percentage_1', 
            '20_to_24_years_percentage_1', '25_to_29_years_percentage_1', '30_to_34_years_percentage_1', 
            '35_to_39_years_percentage_1', '40_to_44_years_percentage_1', '45_to_49_years_percentage_1', 
            '50_to_54_years_percentage_1', '55_to_59_years_percentage_1', '60_to_64_years_percentage_1', 
            '65_to_69_years_percentage_1', '70_to_74_years_percentage_1', '75_to_79_years_percentage_1', 
            '80_to_84_years_percentage_1', '85_and_over_percentage_1', '16_and_over_percentage_1', 
            '18_and_over_percentage_1', '21_and_over_percentage_1', '62_and_over_percentage_1', 
            '65_and_over_percentage_1', 'female_population_percentage', 'under_5_years_percentage_2', 
            '5_to_9_years_percentage_2', '10_to_14_years_percentage_2', '15_to_19_years_percentage_2', 
            '20_to_24_years_percentage_2', '25_to_29_years_percentage_2', '30_to_34_years_percentage_2', 
            '35_to_39_years_percentage_2', '40_to_44_years_percentage_2', '45_to_49_years_percentage_2', 
            '50_to_54_years_percentage_2', '55_to_59_years_percentage_2', '60_to_64_years_percentage_2', 
            '65_to_69_years_percentage_2', '70_to_74_years_percentage_2', '75_to_79_years_percentage_2', 
            '80_to_84_years_percentage_2', '85_and_over_percentage_2', '16_and_over_percentage_2', 
            '18_and_over_percentage_2', '21_and_over_percentage_2', '62_and_over_percentage_2', 
            '65_and_over_percentage_2', 'both_sexes_percentage', 'male_percentage', 'female_percentage', 
            'one_race_percentage', 'white_percentage', 'black_african_american_percentage', 
            'american_indian_alaska_native_percentage', 'asian_percentage', 
            'native_hawaiian_pacific_islander_percentage', 'some_other_race_percentage', 'two_or_more_races_percentage', 
            'total_races_tallied_percentage', 'white_combined_percentage', 'black_combined_percentage', 
            'american_indian_combined_percentage', 'asian_combined_percentage', 
            'native_hawaiian_combined_percentage', 'some_other_race_combined_percentage', 
            'hispanic_or_latino_any_race_percentage', 'not_hispanic_or_latino_percentage', 'hispanic_or_latino_percentage', 
            'white_alone_percentage', 'black_african_american_alone_percentage', 'american_indian_alaska_native_alone_percentage', 
            'asian_alone_percentage', 'native_hawaiian_alone_percentage', 'some_other_race_alone_percentage', 
            'two_or_more_races_percentage_1', 'not_hispanic_or_latino_percentage_1', 'white_alone_percentage_1', 
            'black_african_american_alone_percentage_1', 'american_indian_alaska_native_alone_percentage_1', 
            'asian_alone_percentage_1', 'native_hawaiian_alone_percentage_1', 'some_other_race_alone_percentage_1', 
            'two_or_more_races_percentage_2', 'in_households_percentage', 'householder_percentage', 
            'opposite_sex_spouse_percentage', 'same_sex_spouse_percentage', 'opposite_sex_unmarried_partner_percentage', 
            'same_sex_unmarried_partner_percentage', 'child_percentage', 'under_18_years_percentage', 
            'grandchild_percentage', 'under_18_years_percentage_1', 'other_relatives_percentage', 'non_relatives_percentage', 
            'in_group_quarters_percentage', 'institutionalized_population_percentage', 'male_percentage_1', 
            'female_percentage_1', 'noninstitutionalized_population_percentage', 'male_percentage_2', 
            'female_percentage_2', 'total_households_percentage', 'married_couple_household_percentage', 
            'with_children_under_18_percentage', 'cohabiting_couple_household_percentage', 
            'with_children_under_18_percentage_1', 'male_householder_no_spouse_percentage', 'living_alone_percentage', 
            '65_and_over_percentage_3', 'with_children_under_18_percentage_2', 'female_householder_no_spouse_percentage', 
            'living_alone_percentage_1', '65_and_over_percentage_4', 'with_children_under_18_percentage_3', 
            'households_with_individuals_under_18_percentage', 'households_with_individuals_65_and_over_percentage', 
            'total_housing_units_percentage', 'occupied_housing_units_percentage', 'vacant_housing_units_percentage', 
            'for_rent_percentage', 'rented_not_occupied_percentage', 'for_sale_only_percentage', 'sold_not_occupied_percentage', 
            'for_seasonal_recreational_use_percentage', 'all_other_vacants_percentage', 'homeowner_vacancy_rate_percentage', 
            'rental_vacancy_rate_percentage', 'occupied_housing_units_percentage_1', 'owner_occupied_housing_units_percentage', 
            'renter_occupied_housing_units_percentage'
        ],
        'demo_add': [
            'county_name', 'population_january_2023', 'median_household_income_2021', 
            'race_ethnicity_american_indian_2023', 'race_ethnicity_asian_2023', 'race_ethnicity_black_2023', 
            'race_ethnicity_hispanic_2023', 'race_ethnicity_multi_racial_2023', 
            'race_ethnicity_hawaiian_pacific_island_2023', 'race_ethnicity_white_2023', 
            'age_0_5_2023', 'age_6_17_2023', 'age_18_64_2023', 'age_65_plus_2023'
        ],
        'facility': [
            'id', 'county_name', 'facility_count', 'stations', 'professional_np', 'chain_ownership', 
            'survey_count', 'survey_rate', 'facility_star', 'experience_star', 'community_score', 'quality_score', 
            'information_score', 'physician_score', 'staff_score', 'facility_score'
        ],
        'medicare': [
            'id', 'county_name', 'payment_amount', 'payment_percentage', 'payment_per_capita', 'payment_per_user', 
            'standardized_payment_amount', 'standardized_payment_percentage', 'standardized_payment_per_capita', 
            'standardized_payment_per_user', 'user_count', 'user_percentage', 'visits_per_1000'
        ],
        'voter': [
            'id', 'county_name', 'eligible_2018', 'total_registered_2018', 'democratic_2018', 'republican_2018', 
            'american_independent_2018', 'green_2018', 'libertarian_2018', 'peace_and_freedom_2018', 'unknown_2018', 
            'other_2018', 'no_party_preference_2018', 'eligible_2020', 'total_registered_2020', 'democratic_2020', 
            'republican_2020', 'american_independent_2020', 'green_2020', 'libertarian_2020', 'peace_and_freedom_2020', 
            'unknown_2020', 'other_2020', 'no_party_preference_2020', 'eligible_2022', 'total_registered_2022', 
            'democratic_2022', 'republican_2022', 'american_independent_2022', 'green_2022', 'libertarian_2022', 
            'peace_and_freedom_2022', 'unknown_2022', 'other_2022', 'no_party_preference_2022'
        ]
    }
    
    dataframes = {}
    
    for table_name, file_name in file_names.items():
        file_path = os.path.join(base_path, file_name)
        df = pd.read_csv(file_path)
        df.columns = column_name_mapping[table_name]
        if 'id' in df.columns:
            df.drop(columns=['id'], inplace=True)
        df.sort_values(by='county_name', inplace=True)
        df.reset_index(drop=True, inplace=True)
        dataframes[table_name] = df
    dataframes['demo'] = pd.merge(dataframes['demo'], dataframes['demo_add'], on='county_name', how='right')
    dataframes.pop('demo_add')
    return dataframes

class Table:
    def __init__(self, df: pd.DataFrame, views: Dict[str, List[str]]):
        self._df = df
        self._views = views

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
        """Add a new view to the table."""
        self._views[view_name] = columns

    def get_view(self, view_name: str) -> pd.DataFrame:
        """Get a view of the table by name."""
        if view_name in self._views:
            return self._df[self._views[view_name]]
        raise ValueError(f"View '{view_name}' not found")

class Database:
    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = read_dataframes()
        self.views: Dict[str, Dict[str, List[str]]] = self.create_views()
        self.tables: Dict[str, Table] = {}
        for table_name, df in self.dataframes.items():
            self.tables[table_name] = Table(df, self.views.get(table_name, {}))
            setattr(self, table_name, self.tables[table_name])
        self.merged: Optional[pd.DataFrame] = None

    def create_views(self) -> Dict[str, Dict[str, List[str]]]:
        """Create predefined views for each table."""
        views = {
            'ballot': {
                '2018': ['county_name', 'yes_count_2018', 'no_count_2018', 'total_count_2018', 'yes_percentage_2018', 'no_percentage_2018'],
                '2020': ['county_name', 'yes_count_2020', 'no_count_2020', 'total_count_2020', 'yes_percentage_2020', 'no_percentage_2020'],
                '2022': ['county_name', 'yes_count_2022', 'no_count_2022', 'total_count_2022', 'yes_percentage_2022', 'no_percentage_2022'],
                'all_counts': ['county_name', 'yes_count_2020', 'no_count_2020', 'total_count_2020', 'yes_count_2018', 'no_count_2018', 'total_count_2018', 'yes_count_2022', 'no_count_2022', 'total_count_2022'],
                'all_percentages': ['county_name', 'yes_percentage_2020', 'no_percentage_2020', 'yes_percentage_2018', 'no_percentage_2018', 'yes_percentage_2022', 'no_percentage_2022'],
            },
            'demo': {
                'population': ['county_name', 'population_january_2023', 'median_household_income_2021'],
                'race_ethnicity': ['county_name', 'one_race_percentage', 'some_other_race_percentage', 'two_or_more_races_percentage', 'total_races_tallied_percentage', 
                                'white_combined_percentage', 'black_combined_percentage', 'american_indian_combined_percentage', 
                                'asian_combined_percentage', 'native_hawaiian_combined_percentage', 
                                'hispanic_or_latino_any_race_percentage', 'race_ethnicity_american_indian_2023', 
                                'race_ethnicity_asian_2023', 'race_ethnicity_black_2023', 'race_ethnicity_hispanic_2023', 
                                'race_ethnicity_multi_racial_2023', 'race_ethnicity_hawaiian_pacific_island_2023', 
                                'race_ethnicity_white_2023'],
                'age_groups': ['county_name', 'age_0_5_2023', 'age_6_17_2023', 'age_18_64_2023', 'age_65_plus_2023'],
                'age_distribution': ['county_name', 'under_5_years_percentage', '5_to_9_years_percentage', '10_to_14_years_percentage', 
                                    '15_to_19_years_percentage', '20_to_24_years_percentage', '25_to_29_years_percentage', 
                                    '30_to_34_years_percentage', '35_to_39_years_percentage', '40_to_44_years_percentage', 
                                    '45_to_49_years_percentage', '50_to_54_years_percentage', '55_to_59_years_percentage', 
                                    '60_to_64_years_percentage', '65_to_69_years_percentage', '70_to_74_years_percentage', 
                                    '75_to_79_years_percentage', '80_to_84_years_percentage', '85_and_over_percentage', 
                                    '16_and_over_percentage', '18_and_over_percentage', '21_and_over_percentage', 
                                    '62_and_over_percentage', '65_and_over_percentage'],
                'gender_distribution': ['county_name', 'male_population_percentage', 'female_population_percentage'],
                'household_composition': ['county_name', 'in_households_percentage', 'householder_percentage', 'total_households_percentage', 
                                        'married_couple_household_percentage', 'cohabiting_couple_household_percentage', 
                                        'male_householder_no_spouse_percentage', 'female_householder_no_spouse_percentage', 
                                        'households_with_individuals_under_18_percentage', 
                                        'households_with_individuals_65_and_over_percentage', 'median_household_income_2021']
            },
            'facility': {
                'summary': ['county_name', 'facility_count', 'stations', 'professional_np', 'chain_ownership'],
                'ratings': ['county_name', 'facility_star', 'experience_star', 'community_score', 'quality_score', 'information_score', 'physician_score', 'staff_score', 'facility_score']
            },
            'medicare': {
                'payments': ['county_name', 'payment_amount', 'payment_percentage', 'payment_per_capita', 'payment_per_user', 'standardized_payment_amount', 'standardized_payment_percentage', 'standardized_payment_per_capita', 'standardized_payment_per_user'],
                'standardized_payments': ['county_name', 'standardized_payment_amount', 'standardized_payment_percentage', 'standardized_payment_per_capita', 'standardized_payment_per_user'],
                'visits': ['county_name', 'user_count', 'user_percentage', 'visits_per_1000']
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

    def add_view(self, table_name: str, view_name: str, columns: List[str]) -> None:
        """Add a new view to a specific table."""
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
        """Merge multiple views from different tables."""
        merged_df = None
        for table_name, view_name in views_list:
            view_df = self.get_view(table_name, view_name)
            if merged_df is None:
                merged_df = view_df
            else:
                merged_df = pd.merge(merged_df, view_df, on='county_name', how='outer')
        return merged_df

    def merge_all(self) -> pd.DataFrame:
        """Merge all tables into a single dataframe."""
        if self.merged is None:
            self.merged = pd.concat([table() for table in self.tables.values()], axis=1)
            self.merged = self.merged.loc[:,~self.merged.columns.duplicated()].copy()
        return self.merged

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