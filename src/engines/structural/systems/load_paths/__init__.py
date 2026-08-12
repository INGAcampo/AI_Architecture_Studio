from dataclasses import dataclass
from collections import defaultdict,deque

@dataclass(frozen=True,slots=True)
class LoadTransfer:
    source_id:str
    target_id:str
    fraction:float

class LoadPathEngine:
    def __init__(self): self._edges=defaultdict(list)
    def add_transfer(self,t):
        if not 0<t.fraction<=1: raise ValueError("Fracción inválida")
        self._edges[t.source_id].append(t)
    def distribute(self,source_id,load):
        return tuple((t.target_id,load*t.fraction) for t in self._edges.get(source_id,()))
    def path_exists(self,start,end):
        q=deque([start]);seen={start}
        while q:
            n=q.popleft()
            if n==end:return True
            for t in self._edges.get(n,()):
                if t.target_id not in seen:seen.add(t.target_id);q.append(t.target_id)
        return False
