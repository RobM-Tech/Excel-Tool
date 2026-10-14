from excel_tool.functions.compare import has_config_tag
from excel_tool.config.data_config import config_tag

def test_has_config_tag_exact_line_match():
    multiline = (
        "RCAF 7.1\n"
        "USAF 7.0\n"
        "USAF_BASIC 8.1\n"
        "XAFull"
    )
    only_r = (
        "MB 7.0R\n"
        "USAF_BASIC 8.1R\n"
    )

    assert has_config_tag(multiline) is True
    assert has_config_tag(only_r) is False
    assert has_config_tag("") is False
    assert has_config_tag("   ") is False
    assert has_config_tag(config_tag) is True