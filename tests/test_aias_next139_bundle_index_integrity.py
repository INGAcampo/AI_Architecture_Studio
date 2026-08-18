from aias_next139_bundle_index_integrity import BundleIndexIntegrity


def test_integrity_accepts_contiguous_unique_index() -> None:
    result = BundleIndexIntegrity().check([
        {"ordinal": 1, "path": "a"},
        {"ordinal": 2, "path": "b"},
    ])
    assert result["valid"] is True


def test_integrity_rejects_gaps() -> None:
    assert BundleIndexIntegrity().check([{ "ordinal": 2, "path": "a" }])["valid"] is False
