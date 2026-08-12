class SecondOrderAmplification:
    def b1(self, p_n, pe_n, cm=1.0):
        return cm / max(1.0 - p_n/max(pe_n,1e-12), 1e-6)
