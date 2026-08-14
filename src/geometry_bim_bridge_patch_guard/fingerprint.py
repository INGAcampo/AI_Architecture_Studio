from __future__ import annotations

import hashlib
import json


def patch_plan_sha256(patch_plan) -> str:
    payload={
        "destructive":bool(patch_plan.destructive),
        "operations":[
            {
                "op":str(item.op),
                "instance_id":str(item.instance_id),
            }
            for item in patch_plan.operations
        ],
    }

    raw=json.dumps(
        payload,
        sort_keys=True,
        separators=(",",":"),
        ensure_ascii=True,
    ).encode("ascii")

    return hashlib.sha256(raw).hexdigest()
