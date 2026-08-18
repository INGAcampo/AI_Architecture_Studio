class StirrupDesignEngine:
    def required_av_over_s(self,Vu,phi,Vc,fy,d): return max(Vu/phi-Vc,0)/max(fy*d,1e-12)
