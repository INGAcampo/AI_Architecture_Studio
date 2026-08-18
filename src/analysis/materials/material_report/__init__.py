from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class MaterialReport:markdown:str
class MaterialReportEngine:
    def build(self,s,name):return MaterialReport(f'# Advanced Material Plasticity & Damage Report\n\n- Model: {name}\n- Yielded: {s.yielded}\n- Equivalent plastic strain: {s.equivalent_plastic_strain:.6e}\n- Damage: {s.damage:.6f}\n')
