import pytest
import pandas as pd

from excel_tool.functions.load import load_missing_IDs_to_column

def test_load_missing_IDs_to_column():
    test_list = ['Hello', 'World', 'Beautiful', 'Day', 'Line', 'one', 'Line', 'three', 'Spaces', 'everywhere']
    result = load_missing_IDs_to_column(test_list)
    expected = pd.DataFrame({"Missing originating ID": test_list})

    assert result["Missing originating ID"].all() == expected["Missing originating ID"].all()