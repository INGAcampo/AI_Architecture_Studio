class FemDofManager:
 def __init__(self): self.map={}
 def register(self,node,components):
  for c in components:self.map.setdefault((node,c),len(self.map))
 def index(self,node,c): return self.map[(node,c)]
