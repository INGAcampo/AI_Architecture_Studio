from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RailSegment:
    segment_id:str
    length:float
    gradient:float
    radius:float
class RailAlignmentEngine:
    def total_length(self,segments): return sum(s.length for s in segments)
    def max_gradient(self,segments): return max(abs(s.gradient) for s in segments)
    def minimum_radius(self,segments): return min(s.radius for s in segments)
