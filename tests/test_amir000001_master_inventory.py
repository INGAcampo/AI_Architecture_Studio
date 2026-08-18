from pathlib import Path
from aias_master_inventory.catalog import concepts
from aias_master_inventory.evidence import reconcile
from aias_master_inventory.lighthouse import contract
from aias_master_inventory.orchestrator import MasterInventoryOrchestrator
from aias_master_inventory.roadmap import dependency_cycles,waves
from aias_master_inventory.validator import validate
ROOT=Path(__file__).resolve().parents[1]
def test_inventory_is_broad_and_classified():assert len(concepts())>=60 and {"RULE","FOUNDATION","SYSTEM","OFFICE","ENGINEERING_CAPABILITY","FUTURE_VISION","DUPLICATE"}<={r["kind"] for r in concepts()}
def test_inventory_identifiers_dependencies_and_states_are_valid():assert validate(concepts())==[]
def test_dependency_graph_is_acyclic():assert dependency_cycles(concepts())==[]
def test_roadmap_preserves_dependency_ordered_waves():assert len(waves(concepts()))==23 and waves(concepts())[0]["wave"]==0 and waves(concepts())[-1]["wave"]==22
def test_operational_declarations_have_evidence():assert not [r for r in reconcile(ROOT,concepts()) if not r["supported"]]
def test_lighthouse_delivers_engineering_before_level_five():
 c=contract();assert c["status"]=="OPERATING_REFERENCE_FOR_REVIEW" and "drawings" in c["deliverables"] and "calculation_report" in c["deliverables"] and "do not wait" in c["maturity_policy"]
def test_orchestrator_generates_release(tmp_path):
 r=MasterInventoryOrchestrator().execute(ROOT,tmp_path);assert r["validated"] and r["concepts"]>=60 and Path(r["archive"]).is_file() and len(r["sha256"])==64
