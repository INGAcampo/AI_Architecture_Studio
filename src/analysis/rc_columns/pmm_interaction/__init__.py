class PMMInteractionEngine:
    def ratio(self,pu,pn,mux,mnx,muy,mny): return pu/max(pn,1e-12)+mux/max(mnx,1e-12)+muy/max(mny,1e-12)
