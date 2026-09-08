

def list_one_rubric_to_DOORS(Rubric_Originating_IDs, DOORS_Originating_IDs):
    return set(Rubric_Originating_IDs) - set(DOORS_Originating_IDs)

