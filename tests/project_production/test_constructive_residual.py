import json
from pathlib import Path
def test_residual_rules_have_required_traceability():
 p=Path(__file__).parents[2]/'engineering/aias/standards/VE_CONSTRUCTIVE_CONCRETE_PACK/VE_CONSTRUCTIVE_CONCRETE_PACK_1.1_RESIDUAL.json'; data=json.loads(p.read_text()); assert len(data['rules'])==5
 for r in data['rules']: assert all(r[x] for x in ['rule_id','standard','edition','section','inputs','verdict_logic','source_sha256','evidence_locator'])
