class AxialCapacityEngine:
    def nominal(self,fc,ag,ast,fy): return .85*fc*(ag-ast)+fy*ast
    def design(self,pn,phi=.65): return phi*pn
