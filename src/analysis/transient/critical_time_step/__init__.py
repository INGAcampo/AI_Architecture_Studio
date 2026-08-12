from math import sqrt
class CriticalTimeStepEngine:
    def calculate(self,mass,stiffness): return 2*sqrt(mass/max(stiffness,1e-12))
