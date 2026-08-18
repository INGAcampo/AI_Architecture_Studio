class ElementRepository:
 def __init__(self): self.items={}
 def add(self,e): self.items[e.element_id]=e; return e
 def get(self,i): return self.items[i]
