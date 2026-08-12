from dataclasses import dataclass
from collections import defaultdict,deque
@dataclass(frozen=True,slots=True)
class StructuralMember: member_id:str; start_node_id:str; end_node_id:str; section_id:str; material_id:str; member_type:str
class StructuralGraph:
 def __init__(self): self.members={}; self.adjacency=defaultdict(set)
 def add_member(self,m):
  if m.member_id in self.members: raise ValueError('Miembro duplicado')
  self.members[m.member_id]=m; self.adjacency[m.start_node_id].add(m.member_id); self.adjacency[m.end_node_id].add(m.member_id)
 def connected_members(self,n): return tuple(sorted(self.adjacency.get(n,())))
 def connected_nodes(self,n):
  r=set()
  for mid in self.adjacency.get(n,()):
   m=self.members[mid]; r.add(m.end_node_id if m.start_node_id==n else m.start_node_id)
  return tuple(sorted(r))
 def path_exists(self,a,b):
  q=deque([a]); seen={a}
  while q:
   n=q.popleft()
   if n==b:return True
   for x in self.connected_nodes(n):
    if x not in seen: seen.add(x); q.append(x)
  return False
