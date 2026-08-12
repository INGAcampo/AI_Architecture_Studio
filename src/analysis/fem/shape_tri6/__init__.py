class ShapeTri6:
 def evaluate(self,r,s):
  t=1-r-s; return (t*(2*t-1),r*(2*r-1),s*(2*s-1),4*r*t,4*r*s,4*s*t)
