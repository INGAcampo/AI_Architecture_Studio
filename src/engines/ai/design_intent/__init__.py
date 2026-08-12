from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DesignIntent:
    intent_id:str;description:str;priority:int=0
class DesignIntentManager:
    def __init__(self): self._intents={}
    def register(self,intent): self._intents[intent.intent_id]=intent
    def ordered(self): return tuple(sorted(self._intents.values(),key=lambda x:(-x.priority,x.intent_id)))
    def validate(self,checks):
        return tuple(i for i in self.ordered() if not checks.get(i.intent_id,False))
