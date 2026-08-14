from structural_platform_units.normalize import normalize_result_value


def test_kn_to_n_conversion():
    result=normalize_result_value(12.5,"kN","N")
    assert result.value==12500.0
    assert result.canonical_unit=="N"


def test_knm_to_nm_conversion():
    result=normalize_result_value(3.5,"kN*m","N*m")
    assert result.value==3500.0


def test_mm_to_m_conversion():
    result=normalize_result_value(25.0,"mm","m")
    assert result.value==0.025


def test_unknown_unit_conversion_fails_closed():
    failed=False
    try:
        normalize_result_value(1.0,"psi","N")
    except ValueError:
        failed=True
    assert failed is True
