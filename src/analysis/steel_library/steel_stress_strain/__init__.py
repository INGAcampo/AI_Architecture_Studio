class SteelStressStrainModel:
    def stress_mpa(self,strain,fy=345.,e=200000.): return max(-fy,min(fy,e*strain))
