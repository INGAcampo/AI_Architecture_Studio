from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True, slots=True)
class ConnectivityResult:
    node_members:dict
    isolated_nodes:tuple[str,...]
    disconnected_members:tuple[str,...]
    valid:bool

class FrameConnectivityEngine:
    def analyze(self,frame):
        mapping=defaultdict(list)
        disconnected=[]
        for m in frame.members.values():
            if m.start_node_id not in frame.nodes or m.end_node_id not in frame.nodes:
                disconnected.append(m.member_id)
                continue
            mapping[m.start_node_id].append(m.member_id)
            mapping[m.end_node_id].append(m.member_id)
        isolated=tuple(sorted(nid for nid in frame.nodes if not mapping.get(nid)))
        return ConnectivityResult(dict(mapping),isolated,tuple(sorted(disconnected)),not isolated and not disconnected)
