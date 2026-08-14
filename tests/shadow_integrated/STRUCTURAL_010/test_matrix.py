from structural_platform_compare_matrix.matrix import compare_result_maps


def test_matrix_detects_match_and_mismatch():
    matrix=compare_result_maps(
        {"A":100.0,"B":50.0},
        {"A":100.0,"B":60.0},
        abs_tol=0.1,
        rel_tol=0.001,
    )
    assert tuple(row.status for row in matrix.rows)==("MATCH","MISMATCH")
    assert matrix.mismatch_count==1


def test_matrix_detects_missing_keys():
    matrix=compare_result_maps(
        {"A":1.0},
        {"B":2.0},
    )
    assert tuple(row.status for row in matrix.rows)==(
        "MISSING_CANDIDATE",
        "MISSING_BASELINE",
    )


def test_empty_maps_are_valid_empty_comparison():
    matrix=compare_result_maps({}, {})
    assert matrix.rows==()
    assert matrix.mismatch_count==0
