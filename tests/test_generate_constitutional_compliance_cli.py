import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generator_without_component_regenerates_all_definitions():
    result = subprocess.run([sys.executable, "scripts/generate_constitutional_compliance.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert '"component_id": "AEC-000051"' not in result.stdout
    assert '"component_id": "CERTIFICATION-MASTER-PLAN-001"' in result.stdout
