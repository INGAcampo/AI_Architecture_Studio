class ConvergenceCriteria:
 def check(self,residual,increment,ftol=1e-6,dtol=1e-6):return abs(residual)<=ftol and abs(increment)<=dtol
