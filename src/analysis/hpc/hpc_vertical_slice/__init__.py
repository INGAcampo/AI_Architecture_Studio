from dataclasses import dataclass
from analysis.hpc.cg_solver import ConjugateGradientSolver
from analysis.hpc.domain_partition import DomainPartitionEngine
from analysis.hpc.benchmark_suite import BenchmarkSuite
from analysis.hpc.hpc_diagnostics import HPCDiagnosticsEngine
from analysis.hpc.hpc_ai_advisor import HPCAIAdvisor
from analysis.hpc.hpc_report import HPCReportEngine
@dataclass(frozen=True,slots=True)
class Workflow: solution:tuple;run:object;partitions:tuple;diagnostics:object;advice:object;report:object
class HPCVerticalSlice:
    def run(self,A,b,ids,workers=4):
        x,run=ConjugateGradientSolver().solve(A,b);parts=DomainPartitionEngine().partition(ids,workers)
        bench=BenchmarkSuite();speed=bench.speedup(4,1.2);eff=bench.efficiency(4,1.2,workers)
        d=HPCDiagnosticsEngine().inspect(run.converged,eff,.4)
        return Workflow(x,run,parts,d,HPCAIAdvisor().advise(d),HPCReportEngine().build(workers,run.iterations,run.residual,speed,eff))
