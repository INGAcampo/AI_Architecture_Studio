from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RectangularChannel:
    channel_id:str
    width:float
    depth:float
    slope:float
    roughness_n:float
class OpenChannelHydraulicsEngine:
    def area(self,c): return c.width*c.depth
    def wetted_perimeter(self,c): return c.width+2*c.depth
    def hydraulic_radius(self,c): return self.area(c)/self.wetted_perimeter(c)
    def discharge(self,c): return (1/c.roughness_n)*self.area(c)*self.hydraulic_radius(c)**(2/3)*c.slope**0.5
