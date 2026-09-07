from excel_tool.functions import collection

def main():
    DOORS_req = input("Please drop DOORS file here: ")
    # clean DOORS file path
    collection.get_clean_path(DOORS_req)

    USAF_Block_8 = input("Please drop USAF_Block_8 file here: ")
    # clean USAF_Block_8 file path
    collection.get_clean_path(USAF_Block_8)

    print(DOORS_req)
    


if __name__ == "__main__":
    main()