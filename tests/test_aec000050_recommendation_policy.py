import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_constitution_contains_aec000050():
 text=(ROOT/"engineering"/"aeps"/"02_CONSTITUTION"/"AEC-000002-executable-constitution.yaml").read_text(encoding="utf-8");assert "AEC-000050" in text and "VAL-RECOMMEND-000050" in text

def test_recommendation_policy_is_actionable_and_lean():
 policy=json.loads((ROOT/"engineering"/"aias"/"master"/"STRATEGIC_RECOMMENDATION_POLICY.json").read_text(encoding="utf-8"));assert policy["status"]=="ACTIVE" and "recommended action" in policy["required_content"] and policy["suppress_when"]
