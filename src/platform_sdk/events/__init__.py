from dataclasses import dataclass
from collections import defaultdict,deque
@dataclass(frozen=True,slots=True)
class PlatformEvent:
    topic:str; payload:object=None; source:str|None=None
class GlobalEventBus:
    def __init__(self): self._subs=defaultdict(list); self._queue=deque(); self._busy=False
    def subscribe(self,topic,callback): self._subs[topic].append(callback); return callback
    def publish(self,event):
        self._queue.append(event)
        if self._busy:return
        self._busy=True
        try:
            while self._queue:
                e=self._queue.popleft()
                for cb in tuple(self._subs.get(e.topic,()))+tuple(self._subs.get("*",())): cb(e)
        finally:self._busy=False
