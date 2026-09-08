from excel_tool.functions import collection
from excel_tool.functions import load

def main():
    # Get DOORS file path
    DOORS_req = input("Please drop DOORS file here: ")

    # clean DOORS file path
    DOORS_req_clean = collection.get_clean_path(DOORS_req)

    # Get USAF_Block_8 file path
    USAF_Block_8 = input("Please drop USAF_Block_8 file here: ")

    # clean USAF_Block_8 file path
    USAF_Block_8_clean = collection.get_clean_path(USAF_Block_8)

    # create file data
    DOORS_data = collection.create_file_data(DOORS_req_clean)
    USAF_Block_8_data = collection.create_file_data(USAF_Block_8_clean)

    #load workbooks into datafields
    DOORS_df = load.load_workbook(DOORS_data)
    USAF_Block_8_df = load.load_workbook(USAF_Block_8_data)

    print(DOORS_df["ID"])
    #print(USAF_Block_8_df)
if __name__ == "__main__":
    main()