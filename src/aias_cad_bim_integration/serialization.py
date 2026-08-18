"""Versioned neutral JSON interchange serialization with integrity verification."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from .models import BimElement,InterchangeModel
def write(model:InterchangeModel,path:Path)->dict:
    """Write canonical JSON and return its SHA-256 evidence."""
    payload=model.to_dict();data=(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode("utf-8");path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);return {"path":str(path),"sha256":hashlib.sha256(data).hexdigest()}
def read(path:Path,expected_sha256:str|None=None)->InterchangeModel:
    """Read and optionally authenticate a canonical interchange model."""
    data=path.read_bytes()
    if expected_sha256 and hashlib.sha256(data).hexdigest()!=expected_sha256:raise ValueError("interchange_integrity_failure")
    row=json.loads(data);elements=tuple(BimElement(**{**e,"footprint_mm":tuple(tuple(p) for p in e["footprint_mm"])}) for e in row["elements"]);return InterchangeModel(row["model_id"],row["version"],row["units"],elements,row["provenance"])
