"""Deterministic BIM-footprint projection and controlled property synchronization."""
from __future__ import annotations
import hashlib,json
from aias_drawing_framework import Drawing,Layer,Line,Sheet,Text,View
from .models import InterchangeModel,MappingResult

class CadBimBridge:
    """Map neutral BIM elements to canonical drawings with explicit loss evidence."""
    SUPPORTED_TYPES={"Wall","Footing","Slab","Column"}
    def validate(self,model:InterchangeModel)->None:
        """Require unique identity, millimetres and complete source provenance."""
        if not model.model_id or not model.version or model.units!="mm" or not model.provenance.get("source"):raise ValueError("invalid_interchange_model")
        ids=[]
        for element in model.elements:element.validate();ids.append(element.element_id)
        if len(ids)!=len(set(ids)):raise ValueError("duplicate_element_ids")
    def to_drawing(self,model:InterchangeModel,sheet:Sheet)->tuple[Drawing,MappingResult]:
        """Project supported footprints and report every unsupported semantic loss."""
        self.validate(model);entities=[];mappings=[];losses=[]
        for element in model.elements:
            if element.element_type not in self.SUPPORTED_TYPES:losses.append({"element_id":element.element_id,"reason":"unsupported_element_type","element_type":element.element_type});continue
            points=element.footprint_mm
            for index,(start,end) in enumerate(zip(points,points[1:]+points[:1]),1):entities.append(Line(f"{element.element_id}-L{index}","BIM-OBJECTS",start[0],start[1],end[0],end[1]))
            mappings.append({"element_id":element.element_id,"entity_ids":[f"{element.element_id}-L{i}" for i in range(1,len(points)+1)],"geometry":"footprint","properties_preserved":sorted(element.properties)})
        entities.append(Text("BIM-NOTE","ANNOTATION",15,sheet.height_mm-15,"CAD/BIM PROJECTION - REVIEW REQUIRED",3))
        drawing=Drawing(f"DRW-{model.model_id}",model.version,sheet,(Layer("BIM-OBJECTS","#000000",.35),Layer("ANNOTATION","#000000",.18)),(View("BIM-VIEW","BIM PLAN",100,10,10,sheet.width_mm-20,sheet.height_mm-30,model.model_id),),tuple(entities),{"source":model.provenance["source"],"model_id":model.model_id,"model_sha256":self.digest(model)},True)
        return drawing,MappingResult(drawing.drawing_id,tuple(mappings),tuple(losses))
    def synchronize_properties(self,model:InterchangeModel,updates:dict[str,dict],allowed_properties:set[str])->dict:
        """Apply only allowlisted property updates and return a non-mutating change set."""
        self.validate(model);known={x.element_id:x for x in model.elements};changes={};rejected=[]
        for element_id,values in updates.items():
            if element_id not in known:rejected.append({"element_id":element_id,"reason":"unknown_element"});continue
            accepted={k:v for k,v in values.items() if k in allowed_properties};blocked=sorted(set(values)-allowed_properties)
            if accepted:changes[element_id]={"before":{k:known[element_id].properties.get(k) for k in accepted},"after":accepted}
            if blocked:rejected.append({"element_id":element_id,"reason":"property_not_allowlisted","properties":blocked})
        return {"changes":changes,"rejected":rejected,"requires_transaction_commit":True,"professional_review_required":True}
    @staticmethod
    def digest(model):
        """Return a deterministic integrity digest for an interchange model."""
        return hashlib.sha256(json.dumps(model.to_dict(),sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
