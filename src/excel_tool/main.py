from excel_tool.functions import collection, reconcile




def main():
    # Get file paths
    doors_req    = input("Please drop DOORS file here: ")
    rubric       = input("Please drop rubric file here: ")
    sdd          = input("Please drop sdd file here: ")

    # Clean paths
    # If theres a doors file clean the path
    if doors_req:
        doors_req_clean = collection.get_clean_path(doors_req)
    # If theres a rubric file clean the path
    if rubric:
        rubric_clean    = collection.get_clean_path(rubric)
    # If there is a sdd file clean the path
    if sdd:
        sdd_clean       = collection.get_clean_path(sdd)

    ''' 
    If no doors file uploaded build a new rubric.
    Use sdd file to find MCLLR marked for delete.
    MCLLR that isnt marked add to rubric MCLLRs
    In rubric tag MCLLRs from sdd that have the delete tag,
    in new column.
    '''
    if not doors_req:
        return reconcile.run_build_rubric(rubric_clean, sdd_clean)

    '''
    If there is no sdd uploaded run main tool.
    list 1 - in rubric but not in doors.
    list 2 - in doors but not in rubric
    '''
    if not sdd:
        return reconcile.set_diff_reconcile(doors_req_clean, rubric_clean)


    

if __name__ == "__main__":
    main()