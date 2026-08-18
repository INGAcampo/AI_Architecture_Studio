"""Reproducible multidimensional opportunity scoring for ATO."""
from __future__ import annotations

def score(relevance:float,impact:float,reuse:float,acceleration:float,risk:float,evidence:float)->dict:
    """Score an opportunity and flag high-leverage giant-step candidates."""
    values=(relevance,impact,reuse,acceleration,risk,evidence)
    if any(v<0 or v>1 for v in values):raise ValueError("scores_must_be_between_zero_and_one")
    total=100*(.2*relevance+.25*impact+.15*reuse+.2*acceleration+.15*evidence-.15*risk)
    return {"score":round(max(0,total),2),"giant_step":total>=65,"dimensions":{"relevance":relevance,"impact":impact,"reuse":reuse,"acceleration":acceleration,"risk":risk,"evidence":evidence}}
