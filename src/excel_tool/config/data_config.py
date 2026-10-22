from collections import namedtuple

column_names = {
    "oid": "Originating ID",
    "doors_id":    "ID",
    "doors_text":  "Object Text",
    "branch_off":  "Branch Off of",
    "config":      "Configuration"
}

config_tag = "USAF_BASIC 8.1"


File_data = namedtuple('File_data',
                       ['file_name','file_path', 'file_role'])