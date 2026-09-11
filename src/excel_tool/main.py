from excel_tool.functions import collection, load, compare, write



def main():
    # Get DOORS file path
    DOORS_req = input("Please drop DOORS file here: ")

    # clean DOORS file path
    DOORS_req_clean = collection.get_clean_path(DOORS_req)

    # Get USAF_Block_8 file path
    Block_8_Rubric = input("Please drop Block_8_Rubric file here: ")

    # clean USAF_Block_8 file path
    Block_8_Rubric_clean = collection.get_clean_path(Block_8_Rubric)

    # create file data
    DOORS_data = collection.create_file_data(DOORS_req_clean, "DOORS")
    Block_8_Rubric_data = collection.create_file_data(Block_8_Rubric_clean, "RUBRIC")

    # Make a copy of DOORS to keep original safe when writing
    DOORS_out = collection.make_copy_of_file(DOORS_data)

    #load workbooks into datafields
    DOORS_df = load.load_workbook(DOORS_data)
    Block_8_Rubric_df = load.load_workbook(Block_8_Rubric_data)

    # Convert columns to lists
    # Extract multiple-IDs in on cell preserve order
    DOORS_exploded_df = collection.explode_multi_ID_cells(DOORS_df, "Originating ID")

    # Make Rubric ID column a set for quick comparison
    Block_8_Rubric_Originating_IDs = set(Block_8_Rubric_df["Block 8.1 Full"])

    # Pass to list 1 comparison function
    list_one = compare.list_one_rubric_to_DOORS(
                                            Block_8_Rubric_Originating_IDs, 
                                            DOORS_exploded_df["Originating ID"].to_list())

    # Pass to list 2 comparison runction
    list_two = compare.list_2_DOORS_to_rubric(
                                            DOORS_exploded_df,
                                            Block_8_Rubric_Originating_IDs)

    # Pass to list 3 filter
    list_three = compare.compare_obj_text(DOORS_df)

    

    # Added Extra flagging
    # Flag rows in DOORS with multiple Originating IDs in one cell
    # Get the index of rows that have multiple IDs
    flagged_indexs = DOORS_exploded_df.index[DOORS_exploded_df.index.duplicated()].unique()

    flagged_idx_list = collection.flag_multi_ID_cells(DOORS_df, flagged_indexs)

    # Write lists to DOORS on a new sheet
    write.write_df_to_new_sheet(DOORS_out, list_one, "List One")
    write.write_df_to_new_sheet(DOORS_out, list_two[["ID", "Originating ID"]], "List Two")
    write.write_df_to_new_sheet(DOORS_out, list_three, "List Three")
    write.write_df_to_new_sheet(DOORS_out, flagged_idx_list, "List Four")

if __name__ == "__main__":
    main()