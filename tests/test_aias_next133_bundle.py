from aias_next133_bundle import BundleReleaseEvidence


def test_build_is_deterministic_and_local_only() -> None:
    evidence = BundleReleaseEvidence().build(["z-report", "a-report", "a-report"])
    assert evidence == {
        "bundle": "AIAS-NEXT-133",
        "reports": ["a-report", "z-report"],
        "count": 2,
        "external_publication": False,
    }
