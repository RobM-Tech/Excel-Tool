import pandas as pd

from excel_tool.config.data_config import config_tag, column_names

def compare_obj_text(df):
    df_copy = df.copy()

    # Standardize to lowercase
    lower_case_col = df_copy[column_names["doors_text"]].str.lower()

    # Find all duplicates
    all_dup_text = lower_case_col.duplicated(keep=False)

    # Filter n/a out
    dup_text = all_dup_text & (lower_case_col != "n/a") & df_copy[column_names["doors_text"]].notna()

    return df_copy[dup_text]

# Check if tag is in Config 
def has_config_tag(config_str):
    if config_str == "":
        return False
    
    config_str = config_str.splitlines()

    for s in config_str:
        if s.strip() == config_tag:
            return True

    return False
        

