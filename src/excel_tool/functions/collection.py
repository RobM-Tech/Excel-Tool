import platform
from pathlib import Path
from excel_tool.config.data_config import File_data
from excel_tool.functions.load import load_workbook

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




def create_file_data(clean_fp):
    if "doors" in clean_fp.name.lower():
        DOORS = File_data(file_name=clean_fp.name, file_path=clean_fp)
        return DOORS
    else:
        Block_8_Rubric = File_data(file_name=clean_fp.name, file_path=clean_fp)
        return Block_8_Rubric

    

    