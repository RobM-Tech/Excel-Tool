import pandas as pd

def list_one_rubric_to_DOORS(Rubric_Originating_IDs, DOORS_Originating_IDs):
    missing_IDs = list((Rubric_Originating_IDs) - set(DOORS_Originating_IDs))

    return pd.DataFrame({"Originating ID": missing_IDs})


#List 2: each Originating ID present in DOORS but not in the Rubric 
# (one output row per ID after splitting multi-value cells). 
# Multi-ID source rows are also reported on the flag sheet.
def list_2_DOORS_to_rubric(exploded_df ,Rubric_set):
    missing_IDs = []

    for idx, row in exploded_df.iterrows():
        if row["Originating ID"] not in Rubric_set:
            missing_IDs.append(row)

    return pd.DataFrame(missing_IDs)


def compare_obj_text(df):
    df_copy = df.copy()

    # Standardize to lowercase
    lower_case_col = df_copy["Object Text"].str.lower()

    # Find all duplicates
    all_dup_text = lower_case_col.duplicated(keep=False)

    # Filter n/a out
    dup_text = all_dup_text & (lower_case_col != "n/a") & df_copy["Object Text"].notna()

    return df_copy[dup_text]
