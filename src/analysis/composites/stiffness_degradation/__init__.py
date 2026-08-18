class StiffnessDegradationEngine:
    def degrade(self,value,damage): return value*max(0.0,1-min(damage,.999999))
