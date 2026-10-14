import pytest
import pandas as pd
from pathlib import Path
from excel_tool.functions.collection import (get_clean_path, 
                                             create_file_data, 
                                             explode_multi_ID_cells, 
                                             helper_obj_dict,
                                             helper_branch_off_map)

#Test get_clean_path()

def test_get_clean_path_normal(tmp_path):
    # Create a real temporary .xlsx file for the test
    test_file = tmp_path / "USAF_Block_8_1_DOORS_Reqs.xlsx"
    test_file.write_text("dummy content")   # file must exist on disk

    raw = str(test_file)
    result = get_clean_path(raw)

    assert isinstance(result, Path)
    assert result == test_file
    assert result.is_file()


def test_get_clean_path_quoted(tmp_path):
    
    test_file = tmp_path / "USAF_Block_8_1_DOORS_Reqs.xlsx"
    test_file.write_text("dummy content")   

    raw = f'"{test_file}"'
    result = get_clean_path(raw)

    assert isinstance(result, Path)
    assert result == test_file
    assert result.is_file()


def test_get_clean_path_windows_style(tmp_path):
    test_file = "USAF_Block_8_1_DOORS_Reqs.xlsx"
    # Create a real temp .xlsx so is_file() passes
    test_file = tmp_path / "USAF_Block_8_1_DOORS_Reqs.xlsx"
    test_file.write_text("placeholder")

    result = get_clean_path(str(test_file))

    assert isinstance(result, Path)
    assert result == test_file
    assert result.is_file()
    assert result.suffix.lower() == ".xlsx"


# Test create_file_data()

def test_create_file_data_DOORS():
    test_file = "USAF_Block_8_1_DOORS_Reqs.xlsx"
    
    raw = Path(f"c:/Users/Rob/Desktop/excel sheets/{test_file}")
    result = create_file_data(raw, "DOORS")

    assert result.file_name == test_file
    assert result.file_path == raw
    assert result.file_role == "DOORS"

def test_create_file_data_Block_8_Rubric():
    test_file = "USAF_Block_8_1_Rubric.xlsx"
    
    raw = Path(f"c:/Users/Rob/Desktop/excel sheets/{test_file}")
    result = create_file_data(raw, "RUBRIC")

    assert result.file_name == test_file
    assert result.file_path == raw
    assert result.file_role == "RUBRIC"
# Test explode_multi_ID_cells()

def test_explode_multi_ID_cells():
    df = pd.DataFrame({
        "doc_id": [1, 2, 3, 4],
        "raw_text": [
            "Hello World\nBeautiful Day",
            "Line one\n\nLine three",
            "  Spaces  everywhere  \n",
            None,
        ],
    })

    result = explode_multi_ID_cells(df, "raw_text")

    expected_values = [
        "Hello", "World", "Beautiful", "Day",
        "Line", "one", "Line", "three",
        "Spaces", "everywhere",
    ]

    assert list(result["raw_text"]) == expected_values
    assert list(result["doc_id"]) == [1, 1, 1, 1, 2, 2, 2, 2, 3, 3]


# Test helper_obj_dict
def test_helper_obj_dict_merges_tagged_oids():
    df = pd.DataFrame(
        {
            "Originating ID": [
                "MCS87158",
                "MCS87158 (MB 5.4)",
                "MCS90460 (MB 5.4)",
            ],
            "ID": [
                "MCLLR109223",
                "MCLLR138432",
                "MCLLR128503",
            ],
        }
    )

    result = helper_obj_dict(df, "Originating ID", "ID")

    assert "MCS87158" in result
    assert "MCS87158 (MB 5.4)" not in result
    assert set(result["MCS87158"]) == {"MCLLR109223", "MCLLR138432"}
    assert result["MCS90460"] == ["MCLLR128503"]

# Test helper_branch_off_map()
def test_helper_branch_off_map_parent_to_child_pairs():
    df = pd.DataFrame(
        {
            "Branch Off of": [
                "MCLLR149971",
                "MCLLR109223",
                "MCLLR109223 (MB 5.4)",  # tag should normalize into same parent key
            ],
            "ID": [
                "MCLLR149973",
                "MCLLR138432",
                "MCLLR148259",
            ],
            "Configuration": [
                "MB 6.0\nUSAF_BASIC 8.1\nXAFull",
                "FRANCE KC 6.5.2",
                "",
            ],
        }
    )

    result = helper_branch_off_map(
        df,
        parent_col="Branch Off of",
        child_col1="ID",
        child_col2="Configuration",
    )

    assert "MCLLR149971" in result
    assert ("MCLLR149973", "MB 6.0\nUSAF_BASIC 8.1\nXAFull") in result["MCLLR149971"]

    assert "MCLLR109223" in result
    child_ids = {pair[0] for pair in result["MCLLR109223"]}
    assert child_ids == {"MCLLR138432", "MCLLR148259"}

    # Config left as full string (approach B) — newlines preserved for later splitlines check
    configs = {pair[1] for pair in result["MCLLR109223"]}
    assert "FRANCE KC 6.5.2" in configs
    assert "" in configs