import pytest
from pathlib import Path
from excel_tool.functions.collection import get_clean_path, create_file_data

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


def test_get_clean_path_windows_style():

    test_file = "USAF_Block_8_1_DOORS_Reqs.xlsx"

    raw = f'"c:/Users/Rob/Desktop/excel sheets/{test_file}"'
    result = get_clean_path(raw)

    assert isinstance(result, Path)
    assert result == Path("/mnt/c/Users/Rob/Desktop/excel sheets/USAF_Block_8_1_DOORS_Reqs.xlsx")
    assert result.is_file()
