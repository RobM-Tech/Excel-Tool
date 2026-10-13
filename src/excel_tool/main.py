from excel_tool.functions import collection, load, compare, write



def main():
    # Get file paths
    doors_req       = input("Please drop DOORS file here: ")
    block_8_rubric  = input("Please drop Block_8_Rubric file here: ")
    master          = input("Please drop master file here: ")


    # Clean paths
    doors_req_clean      = collection.get_clean_path(doors_req)
    block_8_rubric_clean = collection.get_clean_path(block_8_rubric)
    master_clean         = collection.get_clean_path(master)

    # Create file data
    doors_data          = collection.create_file_data(doors_req_clean, "DOORS")
    block_8_rubric_data = collection.create_file_data(block_8_rubric_clean, "RUBRIC")
    master_data         = collection.create_file_data(master_clean, "MASTER")

    # Make a copy of DOORS to keep original safe when writing
    doors_out = collection.make_copy_of_file(doors_data)

    # Load workbooks into datafields
    doors_df          = load.load_workbook(doors_data)
    block_8_rubric_df = load.load_workbook(block_8_rubric_data)
    master_df         = load.load_workbook(master_data)

    # Extract multiple-IDs in one cell preserve order
    doors_exploded_df  = collection.explode_multi_ID_cells(doors_df, "Originating ID")
    master_exploded_df = collection.explode_multi_ID_cells(master_df, "Originating ID")


    # Make Rubric ID column a set for quick comparison
    block_8_rubric_originating_ids = set(block_8_rubric_df["Block 8.1 Full"])

    # Pass to list 1 comparison function
    list_one = compare.list_one_rubric_to_DOORS(
                                            block_8_rubric_originating_ids, 
                                            doors_exploded_df["Originating ID"].to_list())
    # pd.merge() dataframes to find all occurances
    list_one_merged_df = list_one.merge(
                                        master_exploded_df[['Originating ID', 'ID']], 
                                        on="Originating ID", 
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
    write.write_df_to_new_sheet(doors_out, list_two[["ID", "Originating ID"]], "List Two")
    write.write_df_to_new_sheet(doors_out, list_three, "List Three")
    write.write_df_to_new_sheet(doors_out, flagged_idx_list, "List Four")

if __name__ == "__main__":
    main()