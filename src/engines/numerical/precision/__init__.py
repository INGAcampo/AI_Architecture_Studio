from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PrecisionPolicy:
    absolute_tolerance:float=1e-12
    relative_tolerance:float=1e-9
    max_iterations:int=1000

class NumericalPrecisionManager:
    def __init__(self,policy=PrecisionPolicy()): self.policy=policy
    def close(self,a,b):
        return abs(a-b)<=max(self.policy.absolute_tolerance,self.policy.relative_tolerance*max(abs(a),abs(b)))
    def vector_close(self,a,b):
        return len(a)==len(b) and all(self.close(x,y) for x,y in zip(a,b))
    def is_zero(self,value): return abs(value)<=self.policy.absolute_tolerance
