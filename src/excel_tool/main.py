from excel_tool.functions import collection, reconcile




def main():
    # Get file paths
    doors_req            = input("Please drop DOORS file here: ")
    block_8_rubric       = input("Please drop Block_8_Rubric file here: ")

    # Get helper file paths
    master               = input("Please drop master file here: ") or None
    obj_with_OID         = input("Please drop ObjectsWithOrigIDNotUSAF81 file here: ") or None
    branch_off           = input("Please drop BranchOffOf file here: ") or None

    # Clean paths
    doors_req_clean      = collection.get_clean_path(doors_req)
    if not block_8_rubric:
        return reconcile.run_mapping(doors_req_clean)

    block_8_rubric_clean = collection.get_clean_path(block_8_rubric)


    
    # Helpers clean paths
    master_clean         = collection.get_clean_path(master)
    obj_with_OID_clean   = collection.get_clean_path(obj_with_OID)
    branch_off_clean     = collection.get_clean_path(branch_off)

    reconcile.run_reconcile(doors_req_clean, 
                            block_8_rubric_clean, 
                            master_clean, 
                            obj_with_OID_clean, 
                            branch_off_clean
                            )

    

if __name__ == "__main__":
    main()