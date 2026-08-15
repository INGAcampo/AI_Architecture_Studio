import json
from pathlib import Path

def test_reference_cases_cannot_be_construction_baselines():
    path=Path('engineering/aias/reference_cases/REFERENCE_CASE_CATALOG.json')
    catalog=json.loads(path.read_text(encoding='utf-8'))
    assert catalog['cases'] and all(x['construction_status']=='NOT_FOR_CONSTRUCTION' for x in catalog['cases'])
    assert 'REAL_PROJECT' in catalog['isolation']
