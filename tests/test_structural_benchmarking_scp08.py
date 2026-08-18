from aias_structural_codes_program import BenchmarkValue,IndependentBenchmark,IndependentBenchmarkValidator


def accepted_benchmark():
    return IndependentBenchmark("BM-FRAME-001","1.0.0","STRUCTURAL_ANALYSIS","Independent Lab","evidence://signed/report-001","closed-form and second solver","P. Reviewer","ACCEPTED",(BenchmarkValue("roof_displacement",12.0,.25,.02,"mm"),BenchmarkValue("base_shear",800.0,5.0,.01,"kN")),True)


def test_independent_benchmark_passes_with_complete_traceable_evidence():
    benchmark=accepted_benchmark();result=IndependentBenchmarkValidator().validate(benchmark,{"roof_displacement":12.2,"base_shear":796.0})
    assert benchmark.validate()==[]
    assert result.status=="VALIDATED_INDEPENDENT"
    assert result.issues==()
    assert result.benchmark_sha256==benchmark.integrity_sha256()
    assert len(result.evidence_sha256())==64
    assert result.professional_release_authorized is False


def test_benchmark_fails_closed_for_missing_or_out_of_tolerance_result():
    result=IndependentBenchmarkValidator().validate(accepted_benchmark(),{"roof_displacement":13.0})
    assert result.status=="REJECTED"
    assert "roof_displacement:outside_tolerance" in result.issues
    assert "base_shear:actual_value_missing" in result.issues


def test_self_generated_or_unreviewed_benchmark_cannot_validate():
    benchmark=IndependentBenchmark("BM","1","STRUCTURAL_ANALYSIS","AIAS","internal://result","same implementation","","PENDING",(BenchmarkValue("x",1,0,.01,"mm"),),False)
    result=IndependentBenchmarkValidator().validate(benchmark,{"x":1})
    assert result.status=="REJECTED"
    assert "independence_not_established" in result.issues


def test_unexpected_and_non_finite_values_are_rejected():
    result=IndependentBenchmarkValidator().validate(accepted_benchmark(),{"roof_displacement":float("nan"),"base_shear":800,"unknown":1})
    assert result.status=="REJECTED"
    assert "roof_displacement:actual_value_non_finite" in result.issues
    assert any(issue.startswith("unexpected_metrics") for issue in result.issues)
