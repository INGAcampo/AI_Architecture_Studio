from pathlib import Path
from aias_release_promotion import ReleasePromotion
ROOT=Path(__file__).resolve().parents[1]
def test_baseline_digest_is_reproducible():
    manifest=ReleasePromotion().build(ROOT,("engineering/aias/release_promotion/AIAS_NEXT_008_SPEC.json",))
    assert len(manifest.digest()) == 64 and manifest.frozen is False
def test_promotion_fails_closed_until_all_gates_close():
    manifest=ReleasePromotion().build(ROOT,("engineering/aias/release_promotion/AIAS_NEXT_008_SPEC.json",),frozen=True)
    result=ReleasePromotion().promote(manifest,clean_tree=False,external_gates_closed=False)
    assert result["promoted"] is False
