import pandas as pd

from excel_tool.config.data_config import File_data


def load_workbook(file: File_data):
    df = pd.read_excel(file.file_path)
    return df


   
    








    