import pandas as pd

import platform
from pathlib import Path

def get_clean_path(file_path):
    # Strip quotes and fix terminal-escaped spaces
    p = file_path.strip().strip("'\"").replace("\\ ", " ")
    
    # convert "C:" to "/mnt/c" ONLY if running on Linux
    if platform.system() == "Linux" and p[1:2] == ":":
        p = f"/mnt/{p[0].lower()}{p[2:]}"

        clean_fp = Path(p)
    return clean_fp




def load_workbook(fp1, fp2):
    clean_fp1 = get_clean_path(fp1)
    clean_fp2 = get_clean_path(fp2)

    df1 = pd.read_excel(clean_fp1)
    df2 = pd.read_excel(clean_fp2)
    print(df1)
    print(df2)