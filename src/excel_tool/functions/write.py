import pandas as pd
from excel_tool.config.data_config import File_data

def write_df_to_new_sheet(file: File_data, df, sheet_name):
    with pd.ExcelWriter(
        file.file_path, 
        engine='openpyxl', 
        mode='a',
        if_sheet_exists='replace'
        ) as f:
        df.to_excel(
            f, 
            sheet_name=sheet_name, 
            index=False
            )