class ConcreteStressStrainModel:
 def stress(self,strain,fc,peak=.002,ultimate=.0035):
  e=abs(strain)
  if e>=ultimate:return 0.0
  if e<=peak:
   r=e/peak;return fc*(2*r-r*r)
  return fc*(1-(e-peak)/(ultimate-peak))
