import pandas as pd

from excel_tool.config.data_config import File_data


def load_workbook(file: File_data):
    
    if file.file_role == "DOORS":
     DOORS_df = pd.read_excel(file.file_path)
     return DOORS_df
    
    else:
        Block_8_Rubric_df = pd.read_excel(file.file_path)
        return Block_8_Rubric_df


   
    








    