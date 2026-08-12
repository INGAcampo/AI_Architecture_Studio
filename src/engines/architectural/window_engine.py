import math
from engines.architectural.opening_engine import OpeningEngine
from engines.geometry.point import Point
from models.architectural.opening import WallOpening
from models.architectural.window import Window
class WindowEngine:
    DEFAULT_WIDTH=1.20; DEFAULT_HEIGHT=1.00; DEFAULT_SILL=0.90
    @classmethod
    def create_window(cls,wall,point,width=1.20,height=1.00,sill_height=0.90,window_type=Window.SLIDING):
        opening=OpeningEngine.create_opening(wall,point,width=width,height=height,sill_height=sill_height,opening_type=WallOpening.WINDOW,name='Hueco de ventana')
        window=Window(opening,width,height,sill_height,window_type); opening.attach_window(window); return window
    @staticmethod
    def _id(window): return getattr(window,'window_id',None)
    @classmethod
    def find_window(cls,wall,window=None,window_id=None):
        target=window_id or cls._id(window)
        for op in list(getattr(wall,'openings',[]) or []):
            c=getattr(op,'window',None)
            if c is window or (c is not None and target is not None and cls._id(c)==target): return c
        return None
    @classmethod
    def contains_window(cls,wall,window=None,window_id=None): return cls.find_window(wall,window,window_id) is not None
    @classmethod
    def add_to_wall(cls,wall,window):
        existing=cls.find_window(wall,window=window)
        if existing is not None:return existing
        window.opening.attach_window(window); OpeningEngine.add_to_wall(wall,window.opening); return window
    @classmethod
    def remove_from_wall(cls,wall,window):
        existing=cls.find_window(wall,window=window)
        return False if existing is None else OpeningEngine.remove_from_wall(wall,existing.opening)
    @classmethod
    def plan_geometry(cls,window):
        op=window.opening; wall=op.host_wall; path=list(getattr(wall,'path',[]) or [])
        if len(path)<2:return None
        i=min(op.segment_index,len(path)-2);p1,p2=path[i],path[i+1];dx,dy=p2.x-p1.x,p2.y-p1.y;l=math.hypot(dx,dy)
        if l<=1e-9:return None
        ux,uy=dx/l,dy/l;nx,ny=-uy,ux;c=op.center_point;hw=window.width/2;ht=max(float(getattr(wall,'thickness',.2)),.01)*.55
        left=Point(c.x-ux*hw,c.y-uy*hw,c.z);right=Point(c.x+ux*hw,c.y+uy*hw,c.z)
        frame=[(Point(left.x-nx*ht,left.y-ny*ht,left.z),Point(left.x+nx*ht,left.y+ny*ht,left.z)),(Point(right.x-nx*ht,right.y-ny*ht,right.z),Point(right.x+nx*ht,right.y+ny*ht,right.z)),(left,right)]
        mullion=(Point(c.x-nx*ht,c.y-ny*ht,c.z),Point(c.x+nx*ht,c.y+ny*ht,c.z))
        return {'frame':frame,'mullion':mullion}
