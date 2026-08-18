from math import sqrt
class VonMises:
 def plane(self,sx,sy,t): return sqrt(sx*sx-sx*sy+sy*sy+3*t*t)
