"""Dependency-safe roadmap and living-knowledge baseline for structural AIAS."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

PROGRAM_ID="STRUCTURAL-CODES-PROGRAM-001"

def program_roadmap()->dict:
    """Return the governed path from reference engines to normative project production."""
    stages=[
      ("SCP-01","Living engineering knowledge","IMPLEMENTED",()),
      ("SCP-02","Structural building canonical model","IMPLEMENTED",("SCP-01",)),
      ("SCP-03","Whole-building analysis contract","IMPLEMENTED",("SCP-02",)),
      ("SCP-04","Beam and column batch design","IMPLEMENTED",("SCP-03",)),
      ("SCP-05","System optimization and consolidated report","IMPLEMENTED",("SCP-04",)),
      ("SCP-06","Licensed load and seismic code-pack framework","IMPLEMENTED_EXTERNAL_CONTENT_REQUIRED",("SCP-03",)),
      ("SCP-07","Licensed concrete, steel and foundation pack framework","IMPLEMENTED_EXTERNAL_CONTENT_REQUIRED",("SCP-04","SCP-06")),
      ("SCP-08","Independent benchmark validation framework","IMPLEMENTED_EXTERNAL_EVIDENCE_REQUIRED",("SCP-05","SCP-07")),
      ("SCP-09","Professional structural production release","IMPLEMENTED_EXTERNAL_APPROVAL_REQUIRED",("SCP-08",)),
      ("MDP-01","Timber, masonry and advanced foundations","IMPLEMENTED_EXTERNAL_CONTENT_REQUIRED",("SCP-09",)),
      ("MDP-02","Geotechnics, rock, hydrology and hydraulic networks","IMPLEMENTED_EXTERNAL_DATA_REQUIRED",("MDP-01",)),
      ("MDP-03","GIS, roads, earthworks and urban infrastructure","IMPLEMENTED_EXTERNAL_DATA_REQUIRED",("MDP-02",)),
      ("GEO-01","Advanced geotechnics and soil-structure interaction","IMPLEMENTED_EXTERNAL_DATA_REQUIRED",("SCP-02",)),
      ("GEO-02","Deep foundations, piles and diaphragm walls","IMPLEMENTED_EXTERNAL_DATA_REQUIRED",("GEO-01",)),
      ("HYD-01","Hydraulic, sanitary and stormwater networks","IMPLEMENTED_EXTERNAL_DATA_REQUIRED",("MDP-02",)),
      ("COORD-01","Executive and multidisciplinary coordination dashboards","IMPLEMENTED",("INT-01","PLT-01")),
      ("INT-01","BIM/IFC neutral synchronization","IMPLEMENTED_NEUTRAL_EXCHANGE",("SCP-02",)),
      ("INT-02","SAP2000, ETABS and Robot governed adapters","IMPLEMENTED_VENDOR_RUNTIME_REQUIRED",("INT-01","SCP-03")),
      ("INT-03","AutoCAD, Revit and Civil 3D governed adapters","IMPLEMENTED_VENDOR_RUNTIME_REQUIRED",("INT-01","MDP-03")),
      ("PLT-01","AI optimization, document automation and distributed compute","IMPLEMENTED",("SCP-05",)),
    ]
    return {"program_id":PROGRAM_ID,"version":"1.0.0","objective":"Open one complete structural building and produce governed analysis, beam design, column design, system optimization and a consolidated technical report.","stages":[{"id":i,"title":t,"status":s,"depends_on":list(d)} for i,t,s,d in stages],"construction_claim":False,"professional_review_required":True}

def knowledge_baseline(root:Path)->dict:
    """Inventory living technical knowledge without treating filenames as validation."""
    groups={"architecture":root/"docs","decisions":root/"engineering","modules":root/"src","tests":root/"tests","standards":root/"engineering/aias/foundation"}
    rows=[]
    for kind,base in groups.items():
        files=sorted(p for p in base.rglob("*") if p.is_file()) if base.exists() else []
        digest=hashlib.sha256("".join(f"{p.relative_to(root).as_posix()}:{hashlib.sha256(p.read_bytes()).hexdigest()}" for p in files).encode()).hexdigest()
        rows.append({"kind":kind,"path":base.relative_to(root).as_posix(),"file_count":len(files),"sha256":digest})
    payload={"catalog_id":"AIAS-LIVING-KNOWLEDGE-001","version":"1.0.0","groups":rows,"authority":"repository_evidence","normative_warning":"Presence does not establish legal applicability, licensed content or professional approval."}
    payload["root_sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();return payload

def validate_program(data:dict)->list[str]:
    """Reject missing dependencies and premature professional claims."""
    ids={x["id"] for x in data.get("stages",[])};issues=[]
    for row in data.get("stages",[]):
        missing=set(row.get("depends_on",()))-ids
        if missing:issues.append(f"{row['id']}:missing:{sorted(missing)}")
    if data.get("construction_claim"):issues.append("premature_construction_claim")
    if not data.get("professional_review_required"):issues.append("professional_review_boundary_missing")
    return issues
