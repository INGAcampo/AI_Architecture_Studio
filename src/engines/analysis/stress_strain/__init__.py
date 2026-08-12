from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class StressStrainResult:
    element_id:str
    axial_force:float
    stress:float
    strain:float

class StressStrainRecovery:
    def axial(self,element_id,axial_force,area,elastic_modulus):
        stress=axial_force/area
        strain=stress/elastic_modulus
        return StressStrainResult(element_id,axial_force,stress,strain)

    def utilization(self,result,allowable_stress):
        return abs(result.stress)/allowable_stress
