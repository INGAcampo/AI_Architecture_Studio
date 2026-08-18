class BilinearTractionSeparation:
    def traction(self,separation,onset,ultimate,peak):
        if separation<=onset:return peak*separation/max(onset,1e-12)
        if separation>=ultimate:return 0.0
        return peak*(ultimate-separation)/max(ultimate-onset,1e-12)
