from math import sqrt
class Gauss3DEngine:
    def points(self):
        p=1/sqrt(3)
        return tuple((x,y,z,1.) for x in (-p,p) for y in (-p,p) for z in (-p,p))
