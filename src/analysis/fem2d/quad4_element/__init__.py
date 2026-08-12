class Quad4ElementEngine:
    def shape(self,xi,eta): return (.25*(1-xi)*(1-eta),.25*(1+xi)*(1-eta),.25*(1+xi)*(1+eta),.25*(1-xi)*(1+eta))