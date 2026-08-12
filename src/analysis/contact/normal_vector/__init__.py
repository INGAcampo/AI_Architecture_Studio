from math import sqrt
class NormalVectorEngine:
    def from_edge_2d(self,a,b):
        x,y=b[0]-a[0],b[1]-a[1];L=max(sqrt(x*x+y*y),1e-12);return (-y/L,x/L)
