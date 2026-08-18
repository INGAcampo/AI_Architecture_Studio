import json
from pathlib import Path
from aias_engineering_system.validator import EngineeringSystemValidator
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"engineering"/"aias"/"foundation"
def result(): return EngineeringSystemValidator().validate(BASE/"AIAS_ENGINEERING_SYSTEM.json",BASE/"AIAS_AES_STANDARDS_REGISTRY.json")
def test_system_and_registry_are_valid(): assert result()["valid"],result()["issues"]
def test_all_company_offices_are_materialized(): assert result()["offices"]==6
def test_initial_normative_standard_set_is_present(): assert result()["standards"]==5
def test_lifecycle_is_complete(): assert result()["lifecycle_states"]==7
def test_professional_boundary_is_explicit(): assert "licensed professional" in json.loads((BASE/"AIAS_ENGINEERING_SYSTEM.json").read_text(encoding="utf-8"))["professional_boundary"]
