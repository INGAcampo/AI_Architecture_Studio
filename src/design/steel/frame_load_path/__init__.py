from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass(frozen=True, slots=True)
class LoadPathResult:
    source_node:str
    support_nodes:tuple[str,...]
    reachable_nodes:tuple[str,...]
    path_exists:bool

class FrameLoadPathEngine:
    def trace(self,frame,source_node,support_nodes):
        graph=defaultdict(set)
        for m in frame.members.values():
            graph[m.start_node_id].add(m.end_node_id)
            graph[m.end_node_id].add(m.start_node_id)
        seen={source_node}; q=deque([source_node])
        while q:
            n=q.popleft()
            for nxt in graph[n]:
                if nxt not in seen:
                    seen.add(nxt); q.append(nxt)
        supports=tuple(sorted(set(support_nodes)&seen))
        return LoadPathResult(source_node,supports,tuple(sorted(seen)),bool(supports))
