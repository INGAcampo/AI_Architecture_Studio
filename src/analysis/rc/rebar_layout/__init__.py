class RebarLayoutEngine:
    def layer_capacity(self,width,cover,db,clear_spacing):
        usable=max(width-2*cover,0); return max(1,int((usable+clear_spacing)/(db+clear_spacing)))
