from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class StructuralFrame:
    frame_id:str
    member_ids:tuple[str,...]
    node_ids:tuple[str,...]

class FrameAssemblyEngine:
    def assemble(self,frame_id,members):
        mids=tuple(sorted(m.member_id for m in members))
        nodes=tuple(sorted({n for m in members for n in (m.start_node_id,m.end_node_id)}))
        return StructuralFrame(frame_id,mids,nodes)
    def is_connected(self,frame,graph):
        if not frame.node_ids:return False
        start=frame.node_ids[0]
        return all(graph.path_exists(start,n) for n in frame.node_ids)
