class ABDMatrixEngine:
    def build_isotropic(self,E,nu,t):
        a=E*t/(1-nu**2); d=E*t**3/(12*(1-nu**2)); z=((0,0,0),(0,0,0),(0,0,0))
        return ((a,0,0),(0,a,0),(0,0,a/2)),z,((d,0,0),(0,d,0),(0,0,d/2))
