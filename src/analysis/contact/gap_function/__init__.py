class GapFunctionEngine:
    def normal_gap(self,s,m,n): return sum((s[i]-m[i])*n[i] for i in range(len(n)))
