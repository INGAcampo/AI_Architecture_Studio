class PeakResponseEngine:
    def peak(self,values): return max((abs(v) for v in values),default=0.0)
