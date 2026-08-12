from math import sin,cos,radians
class MohrCoulombYieldEngine:
    def function(self,s1,s3,phi,c):
        p=radians(phi);return (s1-s3)+(s1+s3)*sin(p)-2*c*cos(p)
