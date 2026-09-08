import pandas as pd

from excel_tool.config.data_config import File_data


def load_workbook(file: File_data):
    
    if "doors" in file.file_name.lower():
     DOORS_df = pd.read_excel(file.file_path)
     return DOORS_df
    
    else:
        USAF_Block_8_df = pd.read_excel(file.file_path)
        return USAF_Block_8_df
    








    