class DoublyReinforcedBeamDesigner:
    def compression_steel(self,required,singly,lever_arm,fy): return max(required-singly,0)/max(fy*lever_arm,1e-12)
