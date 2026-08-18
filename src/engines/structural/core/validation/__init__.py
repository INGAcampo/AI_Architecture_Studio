from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class StructuralIssue: code:str; severity:str; object_id:str; message:str
class StructuralValidationEngine:
 def validate_nodes(self,nodes):
  issues=[]; seen={}
  for n in nodes:
   k=(round(n.x,9),round(n.y,9),round(n.z,9))
   if k in seen: issues.append(StructuralIssue('duplicate_node','warning',n.node_id,f'Coincide con {seen[k]}'))
   else: seen[k]=n.node_id
   if n.mass<0: issues.append(StructuralIssue('negative_mass','error',n.node_id,'Masa negativa'))
  return tuple(issues)
 def validate_graph(self,g):
  return tuple(StructuralIssue('zero_length_member','error',m.member_id,'Nodos idénticos') for m in g.members.values() if m.start_node_id==m.end_node_id)
