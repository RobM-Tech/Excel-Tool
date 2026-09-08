from excel_tool.functions import collection
from excel_tool.functions import load

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

    print(DOORS_data)
    #print(Block_8_Rubric_df)
if __name__ == "__main__":
    main()