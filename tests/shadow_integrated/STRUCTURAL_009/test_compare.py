from structural_platform_compare.compare import compare_scalar_results

def test_equal_values_pass():
    r=compare_scalar_results(10.0,10.0)
    assert r.within_tolerance is True
    assert r.absolute_delta==0.0

def test_small_relative_delta_passes():
    r=compare_scalar_results(1000.0,1000.0001,abs_tol=0.0,rel_tol=1e-6)
    assert r.within_tolerance is True

def test_large_delta_fails():
    r=compare_scalar_results(100.0,120.0,abs_tol=1.0,rel_tol=0.01)
    assert r.within_tolerance is False
