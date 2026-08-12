class PlasticHinge:
 def rotation_state(self,r,ry,ru):
  a=abs(r)
  return 'elastic' if a<=ry else ('plastic' if a<=ru else 'failed')
