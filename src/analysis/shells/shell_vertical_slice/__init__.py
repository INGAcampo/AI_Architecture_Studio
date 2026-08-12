from dataclasses import dataclass
from analysis.shells.shell_domain import ShellLayer
from analysis.shells.laminate_stack import LaminateStack
from analysis.shells.abd_matrix import ABDMatrixEngine
from analysis.shells.laminate_resultants import LaminateResultantsEngine
from analysis.shells.tsai_hill import TsaiHillEngine
from analysis.shells.shell_buckling import ShellBucklingEngine
from analysis.shells.shell_diagnostics import ShellDiagnosticsEngine
from analysis.shells.shell_ai_advisor import ShellAIAdvisor
from analysis.shells.shell_report import ShellReportEngine
@dataclass(frozen=True,slots=True)
class Workflow: layers:tuple; total_thickness:float; membrane_resultants:tuple; bending_resultants:tuple; failure_index:float; buckling_factor:float; diagnostics:object; advice:object; report:object
class ShellVerticalSlice:
    def run(self):
        layers=(ShellLayer('CFRP',.002,0),ShellLayer('CFRP',.002,90),ShellLayer('CFRP',.002,0)); t=LaminateStack().total_thickness(layers); A,B,D=ABDMatrixEngine().build_isotropic(70e9,.3,t); n,m=LaminateResultantsEngine().calculate(A,B,D,(1e-4,5e-5,0),(1e-3,0,0)); fi=TsaiHillEngine().index(100,20,5,600,40,30); bf=ShellBucklingEngine().factor(200,100); d=ShellDiagnosticsEngine().inspect(True,fi,bf); return Workflow(layers,t,n,m,fi,bf,d,ShellAIAdvisor().advise(d),ShellReportEngine().build(len(layers),t,fi,bf))
