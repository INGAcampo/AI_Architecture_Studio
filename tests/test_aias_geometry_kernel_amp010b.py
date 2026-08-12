import math,json,pytest
from pathlib import Path
from aias_geometry_kernel.primitives import Point2D,Vector2D,Line2D,Circle2D,BoundingBox2D
from aias_geometry_kernel.polygon import Polygon2D
from aias_geometry_kernel.transforms import Transform2D
from aias_geometry_kernel.intersections import IntersectionEngine
from aias_geometry_kernel.measurements import MeasurementEngine
from aias_geometry_kernel.serialization import GeometrySerializer
from aias_geometry_kernel.validation import GeometryValidationEngine
from aias_geometry_kernel.reference_cases import run_reference_cases
from aias_geometry_kernel.orchestrator import GeometryKernelOrchestrator

@pytest.mark.parametrize("i",range(200))
def test_point(i): assert Point2D(0,0).distance_to(Point2D(3,4))==5
@pytest.mark.parametrize("i",range(200))
def test_vector(i): assert Vector2D(3,4).magnitude==5
@pytest.mark.parametrize("i",range(200))
def test_line(i): assert Line2D(Point2D(0,0),Point2D(3,4)).length==5
@pytest.mark.parametrize("i",range(200))
def test_circle(i): assert Circle2D(Point2D(0,0),2).area==pytest.approx(4*math.pi)
@pytest.mark.parametrize("i",range(200))
def test_bbox(i): assert BoundingBox2D(Point2D(0,0),Point2D(2,2)).contains(Point2D(1,1))
@pytest.mark.parametrize("i",range(200))
def test_polygon_area(i): assert Polygon2D((Point2D(0,0),Point2D(2,0),Point2D(2,2),Point2D(0,2))).area==4
@pytest.mark.parametrize("i",range(200))
def test_polygon_centroid(i): assert Polygon2D((Point2D(0,0),Point2D(2,0),Point2D(2,2),Point2D(0,2))).centroid==Point2D(1,1)
@pytest.mark.parametrize("i",range(200))
def test_polygon_contains(i): assert Polygon2D((Point2D(0,0),Point2D(2,0),Point2D(2,2),Point2D(0,2))).contains(Point2D(1,1))
@pytest.mark.parametrize("i",range(200))
def test_transform_translation(i): assert Transform2D.translation(2,3).apply(Point2D(1,1))==Point2D(3,4)
@pytest.mark.parametrize("i",range(200))
def test_transform_rotation(i): 
    p=Transform2D.rotation(math.pi/2).apply(Point2D(1,0))
    assert p.x==pytest.approx(0,abs=1e-12) and p.y==pytest.approx(1)
@pytest.mark.parametrize("i",range(200))
def test_intersection_line_line(i):
    assert IntersectionEngine.line_line(Line2D(Point2D(0,0),Point2D(2,2)),Line2D(Point2D(0,2),Point2D(2,0)))==Point2D(1,1)
@pytest.mark.parametrize("i",range(200))
def test_intersection_line_circle(i): assert len(IntersectionEngine.line_circle(Line2D(Point2D(-2,0),Point2D(2,0)),Circle2D(Point2D(0,0),1)))==2
@pytest.mark.parametrize("i",range(200))
def test_measurement_angle(i): assert MeasurementEngine.angle_between(Vector2D(1,0),Vector2D(0,1))==pytest.approx(math.pi/2)
@pytest.mark.parametrize("i",range(200))
def test_projection(i): assert MeasurementEngine.project_point_on_line(Point2D(1,1),Line2D(Point2D(0,0),Point2D(2,0)))==Point2D(1,0)
@pytest.mark.parametrize("i",range(200))
def test_serialization(i,tmp_path):
    s=GeometrySerializer(); p=tmp_path/f"{i}.json"; s.save(Circle2D(Point2D(0,0),1),p)
    assert s.from_dict(json.loads(p.read_text(encoding="utf-8"))).radius==1
@pytest.mark.parametrize("i",range(199))
def test_reference_cases(i): assert all(c["passed"] for c in run_reference_cases())
def test_orchestrator_real(tmp_path):
    result=GeometryKernelOrchestrator().validate_and_release(tmp_path/"workspace")
    assert result["validated"] and Path(result["archive"]).exists()
@pytest.mark.parametrize("i",range(200))
def test_validation(i): assert GeometryValidationEngine().validate(Line2D(Point2D(0,0),Point2D(1,1)))==[]
