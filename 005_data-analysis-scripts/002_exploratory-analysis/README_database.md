# Database Project

This project provides a custom Database class for handling multiple tables, creating views, and performing queries across merged data. It's designed to work with CSV files containing various datasets related to demographics, voting, and other county-level statistics.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Examples](#examples)
6. [Error Handling](#error-handling)


## Project Structure

The project consists of two main files:

1. `database_functions.py`: Contains the core functionality, including the `Database`, `Table`, and utility functions.
2. `database-demo.ipynb`: A Jupyter notebook demonstrating the usage of the Database class.

## Installation

To use this project, you need Python 3.x and the following libraries:

- pandas
- matplotlib
- seaborn

## Usage

1. Access cleaned CSV files in the `009_supplemental/cleaned data` directory.
2. Import and instantiate the `Database` class from `database_functions.py`:

```python
from database_functions import Database

# Initialize the database
db = Database()
```

## Features

- Automatic loading of CSV files
- Creation and management of table views
- Merging of multiple tables and views
- Querying across merged data
- Error handling and best practices

## Examples

Here are some examples of how to use the Database class:

1. Accessing a table:

```python
voter_data = db.voter()
print(voter_data.head())
```

2. Creating a view:

```python
db.voter.add_view("registration_rate", ['year', 'county_name', 'eligible', 'total_registered'])
registration_rate = db.voter.registration_rate
```

3. Merging views:

```python
turnout_df = db.merge_views([('voter', 'registration_rate'), ('ballot', 'casted_votes')])
```

4. Querying the database:

```python
conditions = {'population': lambda x: x > 1000000, 'age_0_5': lambda x: x > 0.05}
result = db.query(conditions, ['county_name', 'population', 'age_0_5'])
```

For more detailed examples, refer to the `database-demo.ipynb` notebook.

## Error Handling

The project includes error handling for common issues such as non-existent tables or views. It's recommended to use the provided `safe_get_view` function to safely access views:

```python
def safe_get_view(db, table_name, view_name):
    if table_name in db.tables:
        table = db.tables[table_name]
        if view_name in table.list_views():
            return table.get_view(view_name)
        else:
            print(f"View '{view_name}' not found in table '{table_name}'")
    else:
        print(f"Table '{table_name}' not found in the database")
    return None
```

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the existing style and includes appropriate tests and documentation.

## License

[Specify your license here, e.g., MIT, GPL, etc.]
