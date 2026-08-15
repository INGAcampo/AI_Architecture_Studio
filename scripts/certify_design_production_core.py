"""Generate deterministic synthetic evidence for the design production core."""
from pathlib import Path

from aias_project_production.certification import certify_design_production_core


if __name__ == "__main__":
    root = Path("engineering/aias/design_production_core_certification")
    result = certify_design_production_core(root)
    print(result["verdict"])
