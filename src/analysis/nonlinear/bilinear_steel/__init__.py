class BilinearSteelModel:
 def stress(self,strain,E,fy,b=.01):
  ey=fy/E
  if abs(strain)<=ey:return E*strain
  s=1 if strain>=0 else -1
  return s*(fy+E*b*(abs(strain)-ey))
