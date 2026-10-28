import pytest
import pandas as pd
from pathlib import Path
from excel_tool.config.data_config import column_names
from excel_tool.functions.collection import (get_clean_path, 
                                             create_file_data, 
                                             explode_multi_ID_cells
                                             )

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

def test_create_file_data_rubric():
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