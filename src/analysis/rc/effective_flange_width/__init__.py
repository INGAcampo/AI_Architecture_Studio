class EffectiveFlangeWidthEngine:
    def calculate(self,span,web_width,slab_thickness): return min(span/4,web_width+16*slab_thickness)
