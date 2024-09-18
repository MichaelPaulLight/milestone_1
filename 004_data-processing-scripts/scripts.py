
def update_df(main_df, target_df, on_key):
    """
    Function to update a main dataframe with values from a target dataframe based on a common key.
    """
    main_df = main_df.merge(target_df, on = on_key)
    return main_df

def create_table(origin_df, columns, labels=None):
    if labels is None:
        labels = columns
    
    # Create a dictionary for renaming: {current_name: new_name}
    rename_dict = dict(zip(columns, labels))
    
    # Select the columns and rename them
    table_df = origin_df[columns].rename(columns=rename_dict)
    
    return table_df
    