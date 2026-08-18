from structural_platform_exchange.contracts import StructuralResultRecord
from structural_platform_audit.equilibrium import audit_force_equilibrium
from structural_platform_audit.quality import audit_result_records


def test_force_equilibrium_passes_balanced_system():
    audit=audit_force_equilibrium(-10000.0,10000.0,tolerance_n=1e-9)
    assert audit.passed is True
    assert audit.residual_n==0.0


def test_force_equilibrium_detects_residual():
    audit=audit_force_equilibrium(-10000.0,9990.0,tolerance_n=1.0)
    assert audit.passed is False
    assert audit.residual_n==-10.0


def test_result_quality_accepts_valid_records():
    records=(
        StructuralResultRecord("B1","M3",100.0,"N*m","ULS"),
    )
    assert audit_result_records(records)==()


def test_result_quality_detects_nonfinite_value():
    records=(
        StructuralResultRecord("B1","M3",float("nan"),"N*m","ULS"),
    )
    issues=audit_result_records(records)
    assert len(issues)==1
    assert issues[0].code=="NONFINITE_VALUE"
