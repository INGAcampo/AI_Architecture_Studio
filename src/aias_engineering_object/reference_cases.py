"""Reproducible isolated-footing fixture and kernel acceptance reference cases."""
from __future__ import annotations
from .factory import EngineeringObjectFactory
from .models import Material, Load
from .validation import EngineeringObjectValidator
from .adapters import GeometryKernelAdapter, ECFAdapter
from .state import StateMachine
from .traceability import TraceabilityEngine

def build_reference_object():
    """Create a traceable rectangular footing with concrete and a vertical service load."""
    return EngineeringObjectFactory().create(
        object_type="ISOLATED_FOOTING",
        name="Reference Isolated Footing",
        geometry={"type":"Rectangle","width":2.0,"length":2.5,"thickness":0.5,"unit":"m"},
        properties={"soil_allowable_pressure":200.0,"soil_unit":"kPa"},
        materials=[Material("MAT-CONC-001","Concrete 30 MPa","CONCRETE",{"fc":30.0},{"fc":"MPa"})],
        loads=[Load("LOAD-001","SERVICE_VERTICAL",800.0,"kN",(0.0,0.0,-1.0))],
        traceability={
            "requirements":["REQ-EOK-001"],
            "knowledge_units":["EKU-000001"],
            "calculation_units":["CKU-000001"],
            "geometry_source":"AMP-010B",
            "deliverables":["QA","TECHNICAL_FILE","TRACEABILITY"]
        }
    )

def run_reference_cases():
    """Exercise identity, validation, geometry, loading, calculation, state and traceability."""
    obj=build_reference_object()
    cases=[]
    cases.append({"id":"EOC-000001","passed":obj.object_id.startswith("EO-")})
    cases.append({"id":"EOC-000002","passed":EngineeringObjectValidator().validate(obj)==[]})
    cases.append({"id":"EOC-000003","passed":GeometryKernelAdapter().area(obj)==5.0})
    cases.append({"id":"EOC-000004","passed":ECFAdapter().total_vertical_load(obj)==800.0})
    cases.append({"id":"EOC-000005","passed":ECFAdapter().bearing_pressure(obj)==160.0})
    sm=StateMachine(); sm.transition(obj.state,"VALIDATED"); sm.transition(obj.state,"CALCULATED")
    cases.append({"id":"EOC-000006","passed":obj.state.calculation_status=="COMPLETE"})
    cases.append({"id":"EOC-000007","passed":"CKU-000001" in TraceabilityEngine().matrix(obj)["calculation_units"]})
    cases.append({"id":"EOC-000008","passed":obj.state.revision==2})
    return cases
