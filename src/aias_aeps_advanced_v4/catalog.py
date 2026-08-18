"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from dataclasses import dataclass, field
from .models import DomainTemplate

@dataclass(slots=True)
class EngineeringAssetCatalog:
    """Execute the public EngineeringAssetCatalog operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    templates: dict[str, DomainTemplate] = field(default_factory=dict)
    assets: dict[str, dict] = field(default_factory=dict)

    def register_template(self, template: DomainTemplate) -> None:
        """Add template to advanced AEPS production, governance and observability while enforcing identity constraints."""
        if template.template_id in self.templates:
            raise ValueError(f"Duplicate template: {template.template_id}")
        self.templates[template.template_id] = template

    def get_template(self, template_id: str) -> DomainTemplate:
        """Return template from advanced AEPS production, governance and observability using deterministic lookup rules."""
        return self.templates[template_id]

    def register_asset(self, asset_id: str, payload: dict) -> None:
        """Add asset to advanced AEPS production, governance and observability while enforcing identity constraints."""
        if asset_id in self.assets:
            raise ValueError(f"Duplicate asset: {asset_id}")
        self.assets[asset_id] = payload

    def search(self, text: str) -> tuple[str, ...]:
        """Return search from advanced AEPS production, governance and observability using deterministic lookup rules."""
        text = text.lower()
        matches = []
        for key, value in self.assets.items():
            if text in key.lower() or text in json_text(value).lower():
                matches.append(key)
        return tuple(sorted(matches))

def json_text(value: dict) -> str:
    """Execute the public json_text operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    import json
    return json.dumps(value, sort_keys=True)
