class CohesiveZoneModel:
    def traction(self,separation,stiffness,damage): return stiffness*separation*max(0.0,1-damage)
