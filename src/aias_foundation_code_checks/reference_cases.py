"""Acceptance cases covering validation, registry, checks, reinforcement and legal gates."""
from .reference_pack import generic_reference_pack,reference_input
from .engine import FoundationCodeCheckEngine
from .registry import CodePackRegistry
from .validation import CodeCheckValidator

def run_reference_cases():
    """Execute the reference-only pack and verify its mandatory safety declarations."""
    pack=generic_reference_pack()
    data=reference_input()
    result=FoundationCodeCheckEngine().check(data,pack)
    reg=CodePackRegistry(); reg.register(pack)
    return [
        {"id":"FCC-000001","passed":CodeCheckValidator().validate_pack(pack)==[]},
        {"id":"FCC-000002","passed":reg.get(pack.code_id).title==pack.title},
        {"id":"FCC-000003","passed":len(result.checks)==5},
        {"id":"FCC-000004","passed":result.reinforcement.governing_area_x_mm2>=result.reinforcement.required_area_x_mm2},
        {"id":"FCC-000005","passed":result.reinforcement.governing_area_y_mm2>=result.reinforcement.required_area_y_mm2},
        {"id":"FCC-000006","passed":any(c.check_id=="PUNCHING_SHEAR" for c in result.checks)},
        {"id":"FCC-000007","passed":result.qa["human_review_required"]},
        {"id":"FCC-000008","passed":result.qa["verified_official_required_for_regulated_use"]},
    ]
