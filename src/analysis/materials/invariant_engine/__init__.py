class StressInvariantEngine:
    def mean_stress(self,s): return sum(s[:3])/3
    def deviatoric(self,s):
        p=self.mean_stress(s);return (s[0]-p,s[1]-p,s[2]-p,*s[3:])
    def j2(self,s):
        d=self.deviatoric(s);return .5*(d[0]**2+d[1]**2+d[2]**2)+d[3]**2+d[4]**2+d[5]**2
