import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_constitution_activates_maximum_stewardship_and_ecosystem_experience():
 text=(ROOT/"engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml").read_text(encoding="utf-8");assert "AEC-000052" in text;assert "VAL-STEWARDSHIP-000052" in text and "VAL-EXPERIENCE-000052" in text;assert "installation_iso" in text and "learning_channel" in text

def test_experience_policy_covers_every_requested_surface_without_false_completion():
 policy=json.loads((ROOT/"engineering/aias/master/AIAS_EXPERIENCE_AND_ECOSYSTEM_POLICY.json").read_text(encoding="utf-8"));surfaces={row["id"]:row for row in policy["surface_portfolio"]};assert {"EXP-DESKTOP","EXP-INSTALLER","EXP-ISO","EXP-WEB","EXP-APPS","EXP-SOCIAL","EXP-LEARNING","EXP-BRAND"}<=set(surfaces);assert surfaces["EXP-ISO"]["status"]=="PLANNED" and surfaces["EXP-WEB"]["status"]=="PLANNED";assert len(policy["mandatory_release_evidence"])>=9

def test_master_plan_is_governed_by_latest_continuity_recommendation_and_experience_rules():
 plan=json.loads((ROOT/"engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json").read_text(encoding="utf-8"));assert {"AEC-000049","AEC-000050","AEC-000051","AEC-000052"}<=set(plan["governing_rules"])
