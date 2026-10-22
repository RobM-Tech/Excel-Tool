import pandas as pd

from excel_tool.config.data_config import config_tag, column_names


def list_one_rubric_to_DOORS(Rubric_Originating_IDs, DOORS_Originating_IDs):
    missing_IDs = list((Rubric_Originating_IDs) - set(DOORS_Originating_IDs))

    return pd.DataFrame({column_names["oid"]: missing_IDs})


#List 2: each Originating ID present in DOORS but not in the Rubric  
# Multi-ID source rows are also reported on the flag sheet.
# Checks if any of the muti-IDs are in Rubric, if any pass the OID is OK
def list_2_DOORS_to_rubric(exploded_df ,Rubric_set):
    # Check what rows have an oid thats in Rubric
    in_rubric = exploded_df[column_names["oid"]].isin(Rubric_set)

    # Group by index and check if ANY row in that group passed
    index_passes = in_rubric.groupby(exploded_df.index).transform("any")

    # Keep only only rows where index completly failed to match
    missing_ids = exploded_df[~index_passes]

    # Remove duplicate rows, df
    return missing_ids.drop_duplicates()


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
        
# Being filter walk for list 1
def filter_list_one(l1_oids, map_a, map_b):
    kept = []

    for oid in l1_oids:
        if oid not in map_a:
            kept.append(oid)
            continue

        # List of associated mcllrs to list 1 oid
        mcllrs = map_a[oid]
        # Loop through the mcllrs and check if they meet oids
        if any(is_covered(m, map_b) for m in mcllrs):
            pass # If true dont add

        else:
            kept.append(oid)

    return pd.DataFrame({column_names["oid"]: kept})

def is_covered(start_mcllr, map_b):
    q = [start_mcllr]
    seen = set()
    # Run till we empty q
    while q:
        current = q.pop(0)
        if current in seen:
            continue
        seen.add(current)
        # children of oid in q, id(mcllr), config values
        children = map_b.get(current, [])
        for child_id, config in children:
            if has_config_tag(config):
                return True
            
            # Keep running till match/ no match
            q.append(child_id)

    return False
