import platform
import shutil


from pathlib import Path
from excel_tool.config.data_config import File_data


def get_clean_path(file_path):
    # Strip quotes and fix terminal-escaped spaces
    p = file_path.strip().strip("'\"").replace("\\ ", " ")
    
    # convert "C:" to "/mnt/c" ONLY if running on Linux
    if platform.system() == "Linux" and p[1:2] == ":":
        p = f"/mnt/{p[0].lower()}{p[2:]}"

    clean_fp = Path(p)

    # Check if path and file exsists
    if not clean_fp.is_file():
        raise FileNotFoundError(f"No file found at: {file_path}")
    
    if clean_fp.suffix.lower() != ".xlsx":
        raise ValueError(f"Error: File type not supported, expected .xlsx but got {clean_fp.suffix}")
    
    
    print(f"{clean_fp.name} uploaded")

    return clean_fp


def make_copy_of_file(file: File_data):
    new_file = file.file_path.stem + "_reconciled" + file.file_path.suffix
    new_file_path = file.file_path.parent / new_file
    shutil.copy2(file.file_path, new_file_path)
    role = file.file_role + "_C"
    return create_file_data(new_file_path, role)

def create_file_data(clean_fp, role):
    file_data = File_data(file_name=clean_fp.name, file_path=clean_fp, file_role=role)
    return file_data


def explode_multi_ID_cells(df, col_name):
    # Make copy of df and replace \n with empty space
    df_copy = df.copy()
    # Pattern to catch tags on Originating ID's
    pattern = r'[\w-]+(?:\s*\([^)]+\))?'

    df_copy[col_name] = df_copy[col_name].astype(str).str.findall(pattern)
    explode_df = df_copy.explode(col_name)

    # Drop row if OID cell is empty
    explode_df = explode_df.dropna(subset=[col_name])

    # Clean any empty strings
    explode_df = explode_df[explode_df[col_name] != ""]

    return explode_df


def flag_multi_ID_cells(df, flagged_list):
    df_copy = df.copy()

    return df_copy.loc[flagged_list]




    

