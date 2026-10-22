from excel_tool.functions.compare import has_config_tag, is_covered, filter_list_one
from excel_tool.config.data_config import config_tag, column_names

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


# Test BFS functions for list one
def test_is_covered_and_filter_list_one():
    # Map B: parent → [(child_id, config), ...]
    map_b = {
        "MCLLR_P1": [
            ("MCLLR_C1", f"MB 6.0\n{config_tag}\nXAFull"),
        ],
        "MCLLR_P2": [
            ("MCLLR_C2", "FRANCE KC 6.5.2\nUSAF_BASIC 8.1R"),
        ],
        "MCLLR_P3": [
            ("MCLLR_C3", "NO TAG HERE"),
        ],
        "MCLLR_C3": [
            ("MCLLR_C4", f"{config_tag}"),  # 2-hop cover
        ],
    }

    # --- is_covered ---
    assert is_covered("MCLLR_P1", map_b) is True
    assert is_covered("MCLLR_P2", map_b) is False
    assert is_covered("MCLLR_P3", map_b) is True
    assert is_covered("MCLLR_UNKNOWN", map_b) is False

    # --- filter_list_one ---
    map_a = {
        "OID_COVERED": ["MCLLR_P1"],
        "OID_FAIL": ["MCLLR_P2"],
        "OID_TWO_HOP": ["MCLLR_P3"],
        "OID_MULTI": ["MCLLR_P2", "MCLLR_P1"],
    }
    l1 = ["OID_COVERED", "OID_FAIL", "OID_TWO_HOP", "OID_MULTI", "OID_NOT_IN_A"]

    kept = filter_list_one(l1, map_a, map_b)

    assert list(kept.columns) == [column_names["oid"]]
    kept_oids = kept[column_names["oid"]].tolist()

    assert "OID_NOT_IN_A" in kept_oids
    assert "OID_FAIL" in kept_oids
    assert "OID_COVERED" not in kept_oids
    assert "OID_TWO_HOP" not in kept_oids
    assert "OID_MULTI" not in kept_oids
    assert kept_oids.count("OID_FAIL") == 1