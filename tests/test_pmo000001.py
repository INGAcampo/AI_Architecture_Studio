from pathlib import Path
import pytest
from aias_pmo import PortfolioOffice,PortfolioItem
from aias_pmo.bootstrap import from_master_inventory
ROOT=Path(__file__).resolve().parents[1];POLICY=ROOT/"engineering/aias/pmo/PMO_POLICY.json"
def test_dependency_ready_priority_selection():
 p=PortfolioOffice(POLICY);p.add(PortfolioItem("A","blocked",["X"],strategic_value=1));p.add(PortfolioItem("B","ready",[],strategic_value=.7));assert p.select_next(set()).item_id=="B" and p.select_next({"X"}).item_id=="A"
def test_stage_transition_requires_complete_evidence():
 p=PortfolioOffice(POLICY);p.add(PortfolioItem("A","item"))
 with pytest.raises(ValueError,match="missing_gate_evidence"):p.transition("A","SPECIFIED",{})
 assert p.transition("A","SPECIFIED",{"specification":"SPEC-A"}).stage=="SPECIFIED"
def test_benefit_measurement_is_classified_and_target_aware():
 p=PortfolioOffice(POLICY);p.add(PortfolioItem("A","item"));r=p.measure_benefit("A",100,50,"REFERENCE_ENGINEERING_ESTIMATE");assert r["meets_45_percent_target"] and r["time_reduction"]==.5
def test_master_inventory_is_immediate_real_consumer():
 p=PortfolioOffice(POLICY);result=from_master_inventory(p,ROOT/"engineering/aias/master/inventory/AIAS_MASTER_CONCEPT_INVENTORY.json");assert result["registered"]>=1 and p.select_next(set()) is not None
