class PerformanceEvaluationEngine:
 def classify(self,d,io,ls,cp):
  a=abs(d)
  return 'Immediate Occupancy' if a<=io else ('Life Safety' if a<=ls else ('Collapse Prevention' if a<=cp else 'Collapse'))
