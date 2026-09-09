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
    DOORS_data = collection.create_file_data(DOORS_req_clean)
    Block_8_Rubric_data = collection.create_file_data(Block_8_Rubric_clean)

    #load workbooks into datafields
    DOORS_df = load.load_workbook(DOORS_data)
    Block_8_Rubric_df = load.load_workbook(Block_8_Rubric_data)

    # Convert list 1 needed columns to lists
    # Extract multiple-IDs in on cell preserve order
    DOORS_Originating_IDs = collection.explode_multi_ID_cells(DOORS_df, "Originating ID")
    Block_8_Rubric_Originating_IDs = list(Block_8_Rubric_df["Block 8.1 Full"])

    # Pass to list 1 comparison function
    list_one = list(compare.list_one_rubric_to_DOORS(Block_8_Rubric_Originating_IDs, DOORS_Originating_IDs))

    #Turn list into column
    l1_df = load.load_missing_IDs_to_column(list_one)

    # Write list 1 to DOORS on a new sheet
    write.write_df_to_new_sheet(DOORS_data, l1_df, "List One")

    
    print(DOORS_Originating_IDs)
if __name__ == "__main__":
    main()