from dataclasses import dataclass
from analysis.materials.constitutive_integrator import ConstitutiveIntegrator
from analysis.materials.damage_evolution import DamageEvolutionLaw
from analysis.materials.isotropic_damage import IsotropicDamageEngine
from analysis.materials.material_diagnostics import MaterialDiagnosticsEngine
from analysis.materials.material_ai_advisor import MaterialAIAdvisor
from analysis.materials.material_report import MaterialReportEngine
from analysis.materials.material_state import MaterialState
@dataclass(frozen=True,slots=True)
class Workflow:state:object;diagnostics:object;advice:object;report:object
class MaterialVerticalSlice:
    def run(self,trial=(350.,0,0,0,0,0),G=80000.,y=250.):
        p=ConstitutiveIntegrator().integrate_j2(trial,G,y);d=DamageEvolutionLaw().exponential(max(p.equivalent_plastic_strain,.002),.001,25.)
        s=MaterialState(IsotropicDamageEngine().degrade(p.stress,d),p.plastic_strain,p.equivalent_plastic_strain,d,p.yielded)
        diag=MaterialDiagnosticsEngine().inspect(True,s.damage,s.equivalent_plastic_strain)
        return Workflow(s,diag,MaterialAIAdvisor().advise(diag),MaterialReportEngine().build(s,'J2 Plasticity + Isotropic Damage'))
