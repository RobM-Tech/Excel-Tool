import pandas as pd

from excel_tool.config.data_config import File_data
df_dict = {}

def load_workbook(file: File_data):
    



    DOORS_df = pd.read_excel(file.file_path)
    df_dict["DOORS"] = DOORS_df

    USAF_Block_8_df = pd.read_excel(file.file_path)
    df_dict["USAF_Block_8"] = USAF_Block_8_df

    print(df_dict)







    