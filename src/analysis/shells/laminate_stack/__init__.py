class LaminateStack:
    def total_thickness(self,layers): return sum(layer.thickness for layer in layers)
