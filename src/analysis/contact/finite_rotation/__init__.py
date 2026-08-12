from math import cos,sin
class FiniteRotationEngine:
    def matrix_2d(self,a):
        c,s=cos(a),sin(a);return ((c,-s),(s,c))
