from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Result:
    unity: float
    status: str

class Engine:
    def evaluate(self, demand=50.0, capacity=100.0):
        u=abs(float(demand))/max(abs(float(capacity)),1e-12)
        return Result(u, "PASS" if u<=1 else "FAIL")
