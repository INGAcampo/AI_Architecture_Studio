"""AEC-000049 admission gates for technology opportunities."""
from __future__ import annotations

def evaluate(correct:bool,verifiable:bool,maintainable:bool,compatible:bool,legal_review:str)->dict:
    """Accept only correct, verifiable, maintainable and compatible work."""
    gates={"technically_correct":correct,"verifiable":verifiable,"maintainable":maintainable,"compatible":compatible,"legal_review_acceptable":legal_review in {"NOT_REQUIRED","PASSED","CONDITIONAL_REFERENCE_ONLY"}}
    return {"accepted":all(gates.values()),"gates":gates,"article":"AEC-000049"}
