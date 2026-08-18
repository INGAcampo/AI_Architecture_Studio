from dataclasses import dataclass, field
from enum import Enum

class AssetClass(str, Enum):
    STRUCTURAL = "structural"
    ARCHITECTURAL = "architectural"
    MEP = "mep"
    EQUIPMENT = "equipment"
    SITE = "site"

@dataclass(frozen=True, slots=True)
class AssetRecord:
    asset_id: str
    name: str
    classification: AssetClass
    type_code: str
    location_id: str | None = None
    attributes: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.asset_id.strip() or not self.name.strip() or not self.type_code.strip():
            raise ValueError("Datos obligatorios")

class AssetRegistry:
    def __init__(self):
        self._assets = {}

    def register(self, asset):
        if asset.asset_id in self._assets:
            raise KeyError(asset.asset_id)
        self._assets[asset.asset_id] = asset
        return asset

    def get(self, asset_id):
        return self._assets[asset_id]

    def by_classification(self, classification):
        return tuple(
            asset for asset in self._assets.values()
            if asset.classification is classification
        )

    def by_location(self, location_id):
        return tuple(
            asset for asset in self._assets.values()
            if asset.location_id == location_id
        )
