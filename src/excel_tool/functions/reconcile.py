import pandas as pd
import numpy as np
from excel_tool.config.data_config import column_names
from excel_tool.functions import (collection,
                                  load,
                                  write)

def set_diff_reconcile(doors_path, rubric_path):
    # Create file data
    doors_data          = collection.create_file_data(doors_path, "DOORS")
    rubric_data = collection.create_file_data(rubric_path, "RUBRIC")

    # Make a copy of DOORS to keep original safe when writing 
    # File data is created as well
    doors_out = collection.make_copy_of_file(doors_data)

    # Load workbooks into datafields
    doors_df     = load.load_workbook(doors_data)
    rubric_df    = load.load_workbook(rubric_data)

    # Make ID column a set for quick comparison
    rubric_originating_ids = set(rubric_df[column_names["id"]])
    doors_df_set = set(doors_df[column_names["id"]])

    # Set comparison
    list_one = rubric_originating_ids - doors_df_set
    list_two = doors_df_set - rubric_originating_ids

    # Turn back to Dataframe
    list_one_df = pd.DataFrame({column_names["id"]: sorted(list_one)})
    list_two_df = pd.DataFrame({column_names["id"]: sorted(list_two)})

    # Write list one to new sheet -> in rubric not in doors.
    write.write_df_to_new_sheet(doors_out, list_one_df, "List One")
    # Write list two to new sheet -> in doors not in rubric.
    write.write_df_to_new_sheet(doors_out, list_two_df, "List Two")


def run_build_rubric(rubric_path, sdd_path):
    # Create file data
    sdd_data        = collection.create_file_data(sdd_path, "MASTER")
    rubric_data     = collection.create_file_data(rubric_path, "RUBRIC")

    # Make a copy of DOORS to keep original safe when writing 
    # File data is created as well
    rubric_out = collection.make_copy_of_file(rubric_data)

    # Load to datafields
    sdd_df = load.load_workbook(sdd_data)

    rubric_df = load.load_workbook(rubric_data)

    # Turn data to sets for quick compare
    sdd_mask    = sdd_df[column_names["id"]].str.contains(r"^Delete\s*-\s*", case=False, na=False)
    sdd_del_set = set(
        sdd_df.loc[sdd_mask, column_names["id"]]
        .str.extract(r"(?i)^Delete\s*-\s*(.*)")[0]
        .dropna()
    )
    
    sdd_active_set = set(sdd_df.loc[~sdd_mask, column_names["id"]])
    rubric_set     = set(rubric_df[column_names["id"]])

    # Add active IDs to rubric
    rubric_set_new = rubric_set | sdd_active_set

    # Turn back to dataframe
    rubric_df_new  = pd.DataFrame({column_names["id"]: list(rubric_set_new)})
    sdd_del_df     = pd.DataFrame({column_names["id"]: list(sdd_del_set)})

    # Flag deleted ID's
    rubric_df_new[column_names["del"]] = (
        rubric_df_new[column_names["id"]]
        .isin(sdd_del_df[column_names["id"]])
        .map({True: "Delete", False: ""})
    )

    # Marked for delete but not in rubric
    missing_mask = ~sdd_del_df[column_names["id"]].isin(rubric_df_new[column_names["id"]])
    missing_df   = pd.DataFrame({
        column_names["not"]:
        sdd_del_df.loc[missing_mask, column_names["id"]].reset_index(drop=True)
        })
    
    # Write updated rubric to new sheet with delete tags.
    write.write_df_to_new_sheet(rubric_out, rubric_df_new, "Rec_Rubric")
    # Write any IDs from sdd marked for delete that did not appear in rubric to new sheet.
    write.write_df_to_new_sheet(rubric_out, missing_df, "Not in Rubric")



# Legacy list 3/4 filters to be reused possibly. Delete if never reused
'''
        
        #List three Originating IDs that have the same object text and it is not n/a.
        
        # Pass to list 3 filter
        list_three = compare.compare_obj_text(doors_df)

        
        #List four extra list that shows what rows had multiple originating IDs in one cell
        
        # Added Extra flagging
        # Flag rows in DOORS with multiple Originating IDs in one cell
        # Get the index of rows that have multiple IDs
        flagged_indexs   = doors_exploded_df.index[doors_exploded_df.index.duplicated()].unique()
        flagged_idx_list = collection.flag_multi_ID_cells(doors_df, flagged_indexs)

        write.write_df_to_new_sheet(doors_out, list_three, "List Three")
        write.write_df_to_new_sheet(doors_out, flagged_idx_list, "List Four")
'''