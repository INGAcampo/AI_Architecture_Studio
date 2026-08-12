from math import sqrt
from analysis.materials.invariant_engine import StressInvariantEngine
class J2YieldEngine:
    def equivalent_stress(self,s): return sqrt(3*StressInvariantEngine().j2(s))
    def function(self,s,y): return self.equivalent_stress(s)-y
