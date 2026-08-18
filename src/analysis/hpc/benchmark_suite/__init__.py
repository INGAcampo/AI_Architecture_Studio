class BenchmarkSuite:
    def speedup(self,serial,parallel):return serial/max(parallel,1e-12)
    def efficiency(self,serial,parallel,workers):return self.speedup(serial,parallel)/max(workers,1)
