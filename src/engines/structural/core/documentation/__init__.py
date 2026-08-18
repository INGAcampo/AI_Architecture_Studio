from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class StructuralSchedule: schedule_id:str; columns:tuple[str,...]; rows:tuple[tuple,...]
class StructuralDocumentationEngine:
 def member_schedule(self,g):
  rows=tuple((m.member_id,m.member_type,m.section_id,m.material_id,m.start_node_id,m.end_node_id) for m in sorted(g.members.values(),key=lambda x:x.member_id))
  return StructuralSchedule('structural-members',('id','type','section','material','start','end'),rows)
 def node_schedule(self,nodes):
  rows=tuple((n.node_id,n.x,n.y,n.z,n.mass) for n in sorted(nodes,key=lambda x:x.node_id)); return StructuralSchedule('structural-nodes',('id','x','y','z','mass'),rows)
