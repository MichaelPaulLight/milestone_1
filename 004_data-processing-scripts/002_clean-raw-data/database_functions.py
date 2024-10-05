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

def read_dataframes(directory_path=None):
    

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    if directory_path is None:
        # Default to the '003_data\002_clean-data' directory
        directory_path = os.path.join(project_root, '003_data', '002_clean-data')
    else:
        # If a path is provided, make it absolute relative to the project root
        directory_path = os.path.abspath(os.path.join(project_root, directory_path))
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    file_names = generate_file_names(directory_path)
    
    # Read column names from CSV files
    column_names_dict = {table_name: pd.read_csv(os.path.join(directory_path, file_name), nrows=0).columns.tolist() 
                         for table_name, file_name in file_names.items()}
    
    # Generate column name mappings
    column_name_mapping = generate_column_name_mappings(column_names_dict)
    
    dataframes = {}
    
    for table_name, file_name in file_names.items():
        df = pd.read_csv(os.path.join(directory_path, file_name))
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
    def __init__(self, path=None):
        self.dataframes: Dict[str, pd.DataFrame] = read_dataframes(path)
        self.views: Dict[str, Dict[str, List[str]]] = self.create_views()
        self.tables: Dict[str, Table] = {}
        for table_name, df in self.dataframes.items():
            self.tables[table_name] = Table(df, self.views.get(table_name, {}), self, table_name)
            setattr(self, table_name, self.tables[table_name])
        self.merged: Optional[pd.DataFrame] = None

    def create_views(self) -> Dict[str, Dict[str, List[str]]]:
        """Create predefined views for each table."""
        views = {
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
        """Merge multiple views from different tables using an outer join on 'year' and 'county_name'."""
        dfs_to_merge = [self.get_view(table_name, view_name) for table_name, view_name in views_list]
        
        # Ensure 'year' and 'county_name' columns exist in all dataframes
        for df in dfs_to_merge:
            if 'year' not in df.columns:
                df['year'] = pd.NaT
            if 'county_name' not in df.columns:
                df['county_name'] = ''
        
        # Perform outer join on 'year' and 'county_name'
        merged_df = dfs_to_merge[0]
        for df in dfs_to_merge[1:]:
            merged_df = pd.merge(merged_df, df, on=['year', 'county_name'], how='outer')
        
        # Move 'county_name' and 'year' to the front
        cols = merged_df.columns.tolist()
        cols = ['county_name', 'year'] + [col for col in cols if col not in ['county_name', 'year']]
        merged_df = merged_df[cols]
        
        return merged_df

    def merge_all(self) -> pd.DataFrame:
        """Merge all tables into a single dataframe using an outer join on 'year' and 'county_name'."""
        dfs_to_merge = list(self.dataframes.values())
        
        # Ensure 'year' and 'county_name' columns exist in all dataframes
        for df in dfs_to_merge:
            if 'year' not in df.columns:
                df['year'] = pd.NaT
            if 'county_name' not in df.columns:
                df['county_name'] = ''
        
        # Perform outer join on 'year' and 'county_name'
        merged_df = dfs_to_merge[0]
        for df in dfs_to_merge[1:]:
            merged_df = pd.merge(merged_df, df, on=['year', 'county_name'], how='outer')
        
        # Move 'county_name' and 'year' to the front
        cols = merged_df.columns.tolist()
        cols = ['county_name', 'year'] + [col for col in cols if col not in ['county_name', 'year']]
        merged_df = merged_df[cols]
        
        return merged_df

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