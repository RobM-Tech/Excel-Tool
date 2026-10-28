from collections import namedtuple

column_names = {
    "oid": "Originating ID",
    "id":    "ID",
    "doors_text":  "Object Text",
    "del":         "Delete flag",
    "not":         "Not in Rubric",
    "config":      "Configuration",
    "multi_entry": "is multi entry"
}

config_tag = "USAF_BASIC 8.1"


File_data = namedtuple('File_data',
                       ['file_name','file_path', 'file_role'])