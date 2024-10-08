# California Health Data Analysis Project

This project analyzes health data for California counties, focusing on dialysis facility metrics and Medicare user data. It includes interactive visualizations, data processing, and exploratory data analysis.

## Files

1. `eda_functions.py`: Module containing utility functions for creating choropleth maps.
2. `EDA.ipynb`: Main analysis notebook containing data loading, processing, and visualization code.
3. `missingness_heatmap.ipynb`': Additional analysis notbook to visualize missing values in fascility records dataset

## Dependencies

- pandas
- matplotlib
- seaborn
- plotly
- requests
- json
- sys
- pathlib

## Features

- Creates choropleth maps of California counties
   - Supports both static and animated (with slider) visualizations
   - Uses GeoJSON data for accurate county boundaries
   - Calculates and visualizes stations per capita across counties and years


- Visualizes pairwise relationships of quality of care metrics
   - Analyzes facility records and aggregated facility data

- Creates a heatmap visualization of missing data patterns across years
   - Display the pattern of missing data across different variables and years

## Data Sources

The project uses two main datasets:
1. Facility Records: Detailed information about individual dialysis facilities.
2. Aggregated Facility Data: Summary statistics of facilities at the county level.

## Usage

### Using the Jupyter Notebook

1. Ensure all required dependencies are installed.
2. Set up the correct file structure, including the path to `database_functions.py`.
3. Run the cells in order to perform the following tasks:
   - Load and preprocess facility records data
   - Visualize pairwise relationships of quality of care metrics
   - Analyze aggregated facility data
   - Create choropleth maps of stations per capita

### Using the Choropleth Map Script

1. Prepare your data as a pandas DataFrame with at least a 'county_name' column and the column you want to visualize.
   - Optional: melt columns by a target feature to use with a slider


3. Create a static choropleth map:
   ```python
   fig = choropleth(data, hue_column='your_value_column')
   fig.show()
   ```

4. Create an animated choropleth map with a slider:
   ```python
   fig = choropleth(data, hue_column='your_value_column', slider_column='year')
   fig.show()
   ```

### Using Missing Values Heatmap:

1. Extracts unique years from the dataset and finds the index of the first row for each year :
```python
year_indices = [fascility_records_df[fascility_records_df['year'] == year].index[0] for year in years]
  ```

2. Adds horizontal lines to separate different years
```python
for idx in year_indices[1:]:
    plt.axhline(y=idx, color='gray', linestyle='--', linewidth=2)
  ```

### Customization

You can customize various aspects of the analyses and visualizations, including:
- Selecting different metrics for pairwise relationship plots
- Adjusting the color scales and layouts of the choropleth maps
- You can customize various aspects of the map, including:
   - Assign variables to hue encoding
   - Assign nominal or ordinal variables to slider encoding
   - Assign custom graph title

### Data Requirements:

Your data should include:
- County names matching the official names used in the GeoJSON data
- Values you want to visualize (e.g., percentages, counts)
- If using the slider functionality, a column for the slider variable (e.g., year)


## Key Analyses

1. Basic statistics and data overview of the 'facility records' table
2. Visualization of pairwise relationships of quality of care metrics by chain ownership and profit status
3. Visualization of stations per capita across California counties over time
4. Visualization of missing values across fascilities records dataset
5. Analysis of aggregated facility data, including facility counts and stations per capita

## Note

This project uses custom database functions (`database_functions.py`) and assumes a specific file structure. Ensure that all necessary files and dependencies are in place before running the analyses.
