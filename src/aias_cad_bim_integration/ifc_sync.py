"""Loss-aware neutral IFC synchronization without claiming native vendor certification."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json
from .models import BimElement,InterchangeModel

IFC_TO_AIAS={"IfcWall":"Wall","IfcFooting":"Footing","IfcSlab":"Slab","IfcColumn":"Column","IfcBeam":"Beam"}
AIAS_TO_IFC={value:key for key,value in IFC_TO_AIAS.items()}

@dataclass(frozen=True,slots=True)
class IfcNeutralEntity:
    global_id:str;kind:str;name:str;footprint_mm:tuple[tuple[float,float],...];properties:dict;source_ref:str

@dataclass(frozen=True,slots=True)
class IfcSyncResult:
    model_id:str;changes:tuple[dict,...];conflicts:tuple[dict,...];losses:tuple[dict,...];requires_transaction_commit:bool;professional_review_required:bool;baseline_sha256:str

class NeutralIfcSynchronizer:
    def import_entities(self,model_id:str,version:str,entities:tuple[IfcNeutralEntity,...],source:str)->tuple[InterchangeModel,tuple[dict,...]]:
        if not model_id or not version or not source:raise ValueError("ifc_import_provenance_required")
        ids=[];elements=[];losses=[]
        for row in entities:
            if not row.global_id or not row.kind or not row.name or not row.source_ref:raise ValueError("invalid_ifc_entity_identity")
            ids.append(row.global_id);mapped=IFC_TO_AIAS.get(row.kind)
            if mapped is None:losses.append({"global_id":row.global_id,"reason":"unsupported_ifc_kind","kind":row.kind});continue
            element=BimElement(row.global_id,mapped,row.name,row.footprint_mm,dict(row.properties),row.source_ref,version);element.validate();elements.append(element)
        if len(ids)!=len(set(ids)):raise ValueError("duplicate_ifc_global_id")
        return InterchangeModel(model_id,version,"mm",tuple(elements),{"source":source,"ifc_schema":"IFC4.3","exchange":"NEUTRAL_JSON"}),tuple(losses)
    def export_entities(self,model:InterchangeModel)->tuple[tuple[IfcNeutralEntity,...],tuple[dict,...]]:
        ids=[];rows=[];losses=[]
        for element in model.elements:
            element.validate();ids.append(element.element_id);kind=AIAS_TO_IFC.get(element.element_type)
            if kind is None:losses.append({"element_id":element.element_id,"reason":"unsupported_aias_type","element_type":element.element_type});continue
            rows.append(IfcNeutralEntity(element.element_id,kind,element.name,element.footprint_mm,dict(element.properties),element.source_ref))
        if len(ids)!=len(set(ids)):raise ValueError("duplicate_element_ids")
        return tuple(rows),tuple(losses)
    def synchronize(self,baseline:InterchangeModel,aias:InterchangeModel,ifc:InterchangeModel,allowed_properties:set[str])->IfcSyncResult:
        if not (baseline.model_id==aias.model_id==ifc.model_id):raise ValueError("synchronization_model_identity_mismatch")
        base={x.element_id:x for x in baseline.elements};left={x.element_id:x for x in aias.elements};right={x.element_id:x for x in ifc.elements};changes=[];conflicts=[];losses=[]
        for element_id in sorted(set(base)|set(left)|set(right)):
            if element_id not in base or element_id not in left or element_id not in right:
                losses.append({"element_id":element_id,"reason":"identity_not_present_in_all_models"});continue
            keys=set(base[element_id].properties)|set(left[element_id].properties)|set(right[element_id].properties)
            for key in sorted(keys):
                if key not in allowed_properties:
                    if left[element_id].properties.get(key)!=base[element_id].properties.get(key) or right[element_id].properties.get(key)!=base[element_id].properties.get(key):losses.append({"element_id":element_id,"property":key,"reason":"property_not_allowlisted"})
                    continue
                old=base[element_id].properties.get(key);a=left[element_id].properties.get(key);b=right[element_id].properties.get(key)
                if a!=old and b!=old and a!=b:conflicts.append({"element_id":element_id,"property":key,"baseline":old,"aias":a,"ifc":b})
                elif a!=old or b!=old:changes.append({"element_id":element_id,"property":key,"before":old,"after":a if a!=old else b,"source":"AIAS" if a!=old else "IFC"})
        payload=json.dumps(baseline.to_dict(),sort_keys=True,separators=(",",":"),ensure_ascii=False)
        return IfcSyncResult(baseline.model_id,tuple(changes),tuple(conflicts),tuple(losses),True,True,hashlib.sha256(payload.encode()).hexdigest())
