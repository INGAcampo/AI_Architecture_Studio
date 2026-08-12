class BenzeggaghKenaneEngine:
    def critical_energy(self,gi,gii,gic,giic,eta):
        total=max(gi+gii,1e-12); return gic+(giic-gic)*(gii/total)**eta
