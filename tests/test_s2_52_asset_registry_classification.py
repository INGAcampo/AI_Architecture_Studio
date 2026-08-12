import pytest
from engines.structural.asset_registry import *

@pytest.mark.parametrize("index", range(120))
def test_asset_registry(index):
    registry = AssetRegistry()
    classification = list(AssetClass)[index % len(AssetClass)]
    asset = AssetRecord(
        f"A{index}",
        f"Asset {index}",
        classification,
        f"T{index%9}",
        location_id=f"L{index%4}",
        attributes={"index": index},
    )
    registry.register(asset)
    assert registry.get(asset.asset_id) is asset
    assert asset in registry.by_classification(classification)
    assert asset in registry.by_location(asset.location_id)
