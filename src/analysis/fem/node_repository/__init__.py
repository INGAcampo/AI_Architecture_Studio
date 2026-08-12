class NodeRepository:
 def __init__(self): self.items={}
 def add(self,n): self.items[n.node_id]=n; return n
 def get(self,i): return self.items[i]
