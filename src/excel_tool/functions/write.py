import pandas as pd
import openpyxl
from excel_tool.config.data_config import File_data

def write_df_to_new_sheet(file: File_data, df, sheet_name):
    widths = {'ID': 20, 'Object Text': 50, 'Originating ID': 25}

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
        ws = f.sheets[sheet_name]

        for idx, col_name in enumerate(df.columns, start=1):
            if col_name in widths:
                let = openpyxl.utils.get_column_letter(idx)
                ws.column_dimensions[let].width = widths[col_name]

    print(f"Wrote: {sheet_name} to {file.file_name}")