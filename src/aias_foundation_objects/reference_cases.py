"""Reference objects and acceptance cases for every supported foundation family."""
from .factory import FoundationFactory
from .models import SoilProfile, ColumnSupport
from .validation import FoundationValidator
from .metrics import FoundationMetrics

def reference_objects():
    """Build isolated, combined, strip, mat, pedestal and beam fixtures."""
    soil=SoilProfile(200.0,18.0,30.0,0.0,25.0,3.0)
    c1=ColumnSupport("C1",1.0,1.25,0.4,0.4,800.0,20.0,10.0)
    c2=ColumnSupport("C2",3.0,1.25,0.4,0.4,600.0,15.0,5.0)
    f=FoundationFactory()
    return {
        "isolated":f.isolated(name="ISO-REF",width_m=2.0,length_m=2.5,thickness_m=0.5,soil=soil,support=c1),
        "combined":f.combined(name="COMB-REF",width_m=2.5,length_m=5.0,thickness_m=0.6,soil=soil,supports=[c1,c2]),
        "strip":f.strip(name="STRIP-REF",width_m=1.2,length_m=10.0,thickness_m=0.4,soil=soil,line_load_kn_m=80.0),
        "mat":f.mat(name="MAT-REF",width_m=10.0,length_m=12.0,thickness_m=0.7,soil=soil,supports=[c1,c2]),
        "pedestal":f.pedestal(name="PED-REF",width_m=0.8,length_m=0.8,height_m=1.0,soil=soil,support=c1),
        "beam":f.foundation_beam(name="FB-REF",width_m=0.4,length_m=5.0,depth_m=0.7,soil=soil,supports=[c1,c2]),
    }

def run_reference_cases():
    """Verify object validation, geometry, loading, metadata and volume metrics."""
    objs=reference_objects(); m=FoundationMetrics(); v=FoundationValidator()
    return [
        {"id":"FOL-000001","passed":v.validate(objs["isolated"])==[]},
        {"id":"FOL-000002","passed":objs["isolated"].geometry.area_m2==5.0},
        {"id":"FOL-000003","passed":m.gross_bearing_pressure_kpa(objs["isolated"])==160.0},
        {"id":"FOL-000004","passed":len(objs["combined"].supports)==2},
        {"id":"FOL-000005","passed":objs["strip"].metadata["line_load_kn_m"]==80.0},
        {"id":"FOL-000006","passed":objs["mat"].geometry.area_m2==120.0},
        {"id":"FOL-000007","passed":abs(objs["pedestal"].geometry.volume_m3-0.64)<1e-12},
        {"id":"FOL-000008","passed":objs["beam"].geometry.volume_m3==1.4},
    ]
