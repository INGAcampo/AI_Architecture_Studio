from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class BridgeDeck:
    bridge_id:str
    span_count:int
    span_length:float
    width:float
    thickness:float
class BridgeDeckEngine:
    def total_length(self,b): return b.span_count*b.span_length
    def deck_area(self,b): return self.total_length(b)*b.width
    def concrete_volume(self,b): return self.deck_area(b)*b.thickness
