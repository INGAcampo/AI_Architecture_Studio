import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from engines.geometry.point import Point
from engines.geometry.geometry_builder import GeometryBuilder
p=[Point(0,0,0),Point(5,0,0),Point(5,4,0)]
poly=GeometryBuilder.build_clean_wall_geometry(p,0.2,"center")
assert len(poly)==6, poly
assert abs(poly[1].x-4.9)<1e-7 and abs(poly[1].y-0.1)<1e-7, poly[1]
assert abs(poly[-2].x-5.1)<1e-7 and abs(poly[-2].y+0.1)<1e-7, poly[-2]
print("WALL JOIN 5.0.4.2: pruebas geométricas OK")
