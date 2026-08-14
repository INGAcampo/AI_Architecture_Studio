from structural_platform_compare_matrix.matrix import compare_result_maps
from structural_platform_acceptance.gate import evaluate_structural_acceptance

def test_matching_matrix_is_accepted():
    matrix=compare_result_maps({"A":1.0},{"A":1.0})
    assert evaluate_structural_acceptance(matrix).accepted is True

def test_missing_result_is_rejected():
    matrix=compare_result_maps({"A":1.0},{})
    d=evaluate_structural_acceptance(matrix)
    assert d.accepted is False
    assert d.reason=="missing_results"

def test_mismatch_limit_is_enforced():
    matrix=compare_result_maps({"A":1.0},{"A":2.0},abs_tol=0.0,rel_tol=0.0)
    d=evaluate_structural_acceptance(matrix,max_mismatches=0)
    assert d.accepted is False
    assert d.reason=="mismatch_limit_exceeded"
