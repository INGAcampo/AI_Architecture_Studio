from __future__ import annotations
import hashlib
import json

def decision_trace_sha256(trace)->str:
    payload=[
        {
            "sequence":int(item.sequence),
            "stage":str(item.stage),
            "accepted":bool(item.accepted),
            "reason":str(item.reason),
        }
        for item in trace.events
    ]
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
    return hashlib.sha256(raw).hexdigest()
