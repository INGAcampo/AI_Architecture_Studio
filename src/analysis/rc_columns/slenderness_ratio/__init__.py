from math import sqrt
class SlendernessRatioEngine:
    def radius_of_gyration(self,area,inertia): return sqrt(inertia/max(area,1e-12))
    def calculate(self,k,length,radius): return k*length/max(radius,1e-12)
