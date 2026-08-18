from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class BenchmarkResult:
    benchmark_id:str
    expected:float
    actual:float
    relative_error:float
    passed:bool

class EngineeringBenchmarkSuite:
    def compare(self,benchmark_id,expected,actual,tolerance=1e-6):
        denom=max(abs(expected),1e-12)
        error=abs(actual-expected)/denom
        return BenchmarkResult(benchmark_id,expected,actual,error,error<=tolerance)

    def axial_bar_displacement(self,load,length,area,elastic_modulus):
        return load*length/(area*elastic_modulus)

    def simply_supported_beam_midspan(self,load,length,elastic_modulus,inertia):
        return load*length**3/(48*elastic_modulus*inertia)
