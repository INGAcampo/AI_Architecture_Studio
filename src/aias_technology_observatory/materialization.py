"""Earliest-maturity value actions required by AEC-000049."""
from __future__ import annotations

def earliest_action(opportunity_id:str,accepted:bool,giant_step:bool)->dict:
    """Choose a bounded experiment or reference adapter for an opportunity."""
    if not accepted:return {"opportunity_id":opportunity_id,"action":"HOLD","maturity":"DISCOVERY","reason":"constitutional_gate_failed"}
    return {"opportunity_id":opportunity_id,"action":"IMPLEMENT_REFERENCE_ADAPTER" if giant_step else "RUN_BOUNDED_EXPERIMENT","maturity":"REFERENCE_CAPABILITY","reason":"AEC-000049_immediate_value"}
