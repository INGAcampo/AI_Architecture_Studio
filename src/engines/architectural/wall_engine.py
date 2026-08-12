"""AIAS Architectural Wall Engine — WALL JOIN 5.0.4.2."""
from engines.geometry.point import Point
from engines.geometry.geometry_builder import GeometryBuilder
from models.architectural.wall import Wall

class WallEngine:
    DEFAULT_THICKNESS=0.20; DEFAULT_HEIGHT=3.00; DEFAULT_JUSTIFICATION="center"; MITER_LIMIT=8.0; EPSILON=1.0e-9

    @staticmethod
    def clean_centerline(points):
        result=[]
        for p in points or []:
            copy=Point(p.x,p.y,getattr(p,"z",0.0))
            if result and result[-1].distance_to(copy)<=WallEngine.EPSILON: continue
            result.append(copy)
        return result

    @staticmethod
    def create_wall(points, thickness=DEFAULT_THICKNESS, justification=DEFAULT_JUSTIFICATION, base_level="Nivel 0", height=DEFAULT_HEIGHT):
        points=WallEngine.clean_centerline(points)
        if len(points)<2: raise ValueError("Un muro requiere al menos dos puntos.")
        if float(thickness)<=0: raise ValueError("El espesor del muro debe ser mayor que cero.")
        return Wall(points,thickness,justification,base_level,height)

    @staticmethod
    def create_preview(points,current_point,thickness=DEFAULT_THICKNESS,justification=DEFAULT_JUSTIFICATION):
        values=list(points or [])
        if current_point is not None: values.append(current_point)
        values=WallEngine.clean_centerline(values)
        return Wall(values,thickness,justification) if len(values)>=2 else None

    @classmethod
    def build_wall_data(cls,wall):
        offsets=GeometryBuilder.build_wall_offsets(wall.path,wall.thickness,wall.justification,cls.MITER_LIMIT)
        polygon=GeometryBuilder.build_clean_wall_geometry(wall.path,wall.thickness,wall.justification,cls.MITER_LIMIT)
        return {"centerline":[(Point(a.x,a.y,getattr(a,"z",0.0)),Point(b.x,b.y,getattr(b,"z",0.0))) for a,b in offsets["segments"]],"left":offsets["left"],"right":offsets["right"],"polygon":polygon}

    @classmethod
    def build_clean_polygon(cls,wall):
        cached=getattr(wall,"clean_polygon",None)
        return list(cached) if cached else GeometryBuilder.build_clean_wall_geometry(wall.path,wall.thickness,wall.justification,cls.MITER_LIMIT)

    @staticmethod
    def build_segment_polygons(wall):
        return GeometryBuilder.build_wall_segment_polygons(wall.path,wall.thickness,wall.justification)

    @classmethod
    def build_wall_geometry(cls,wall):
        polygon=cls.build_clean_polygon(wall)
        return [polygon] if polygon else []
