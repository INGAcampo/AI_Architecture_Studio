class KinematicHardeningLaw:
    def update_backstress(self,a,de,H): return tuple(x+H*y for x,y in zip(a,de))
