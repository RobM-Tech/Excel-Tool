from excel_tool.config.data_config import column_names
from excel_tool.functions import (collection,
                                  load,
                                  compare,
                                  write)

def run_reconcile(doors_path, rubric_path, master_path=None, helper_a_path=None, helper_b_path=None):
    # Create file data
    doors_data          = collection.create_file_data(doors_path, "DOORS")
    block_8_rubric_data = collection.create_file_data(rubric_path, "RUBRIC")
    
    # Helpers file data
    master_data         = collection.create_file_data(master_path, "MASTER")
    obj_with_OID_data   = collection.create_file_data(helper_a_path, "NOT_USAF81")
    branch_off_data     = collection.create_file_data(helper_b_path, "BRANCH_OFF")

    # Make a copy of DOORS to keep original safe when writing
    doors_out = collection.make_copy_of_file(doors_data)


    # Load workbooks into datafields
    doors_df          = load.load_workbook(doors_data)
    block_8_rubric_df = load.load_workbook(block_8_rubric_data)
    master_df         = load.load_workbook(master_data)
    # Load helpers into datafields
    obj_with_OID_df   = load.load_workbook(obj_with_OID_data)
    branch_off_df     = load.load_workbook(branch_off_data)

    
    # Extract multiple-IDs in one cell preserve order
    doors_exploded_df  = collection.explode_multi_ID_cells(doors_df, column_names["oid"])
    master_exploded_df = collection.explode_multi_ID_cells(master_df, column_names["oid"])


    # Create helper dicts
    obj_with_OID_dict = collection.helper_obj_dict(obj_with_OID_df, 
                                                   column_names["oid"], 
                                                   column_names["doors_id"]
                                                   )
    branch_off_dict = collection.helper_branch_off_map(branch_off_df, 
                                                       column_names["branch_off"], 
                                                       column_names["doors_id"], 
                                                       column_names["config"]
                                                       )


    # Make Rubric ID column a set for quick comparison
    block_8_rubric_originating_ids = set(block_8_rubric_df["Block 8.1 Full"])


    '''
    List one Originating IDs in the rubric but not in DOORS (optionally enriched with MASTER ID
    Also filterd against two helper files, objectswithnoUSAF and BranchOffof
    '''
    # Pass to list 1 comparison function
    list_one = compare.list_one_rubric_to_DOORS(
                                            block_8_rubric_originating_ids, 
                                            doors_exploded_df[column_names["oid"]].to_list())

    # Run list one against new filter (objwithnoUSAF, BranchOffof)
    list_one_filtered = compare.filter_list_one(list_one[column_names["oid"]].to_list(),
                                                obj_with_OID_dict,
                                                branch_off_dict )

    # pd.merge() dataframes to find all occurances
    list_one_merged_df = list_one_filtered.merge(
                                        master_exploded_df[['Originating ID', 'ID']], 
                                        on=column_names["oid"], 
                                        how="left"
                                       )

    # Pass to list 2 comparison runction
    list_two = compare.list_2_DOORS_to_rubric(
                                            doors_exploded_df,
                                            block_8_rubric_originating_ids)
    
    # Pass to list 3 filter
    list_three = compare.compare_obj_text(doors_df)


    # Added Extra flagging
    # Flag rows in DOORS with multiple Originating IDs in one cell
    # Get the index of rows that have multiple IDs
    flagged_indexs   = doors_exploded_df.index[doors_exploded_df.index.duplicated()].unique()
    flagged_idx_list = collection.flag_multi_ID_cells(doors_df, flagged_indexs)


    # Write lists to DOORS on a new sheet
    write.write_df_to_new_sheet(doors_out, list_one_merged_df, "List One")
    write.write_df_to_new_sheet(doors_out, list_two[[column_names["doors_id"], column_names["oid"]]], "List Two")
    write.write_df_to_new_sheet(doors_out, list_three, "List Three")
    write.write_df_to_new_sheet(doors_out, flagged_idx_list, "List Four")