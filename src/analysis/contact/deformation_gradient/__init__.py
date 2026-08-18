class DeformationGradientEngine:
    def one_dimensional(self,current,reference): return current/max(reference,1e-12)
