from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True, slots=True)
class DenseVector:
    values: tuple[float, ...]

    def __post_init__(self):
        object.__setattr__(self, "values", tuple(float(v) for v in self.values))

    def __len__(self): return len(self.values)
    def __getitem__(self, i): return self.values[i]

    def add(self, other):
        if len(self) != len(other): raise ValueError("Dimensiones incompatibles")
        return DenseVector(tuple(a+b for a,b in zip(self.values, other.values)))

    def subtract(self, other):
        if len(self) != len(other): raise ValueError("Dimensiones incompatibles")
        return DenseVector(tuple(a-b for a,b in zip(self.values, other.values)))

    def scale(self, factor):
        return DenseVector(tuple(float(factor)*v for v in self.values))

    def dot(self, other):
        if len(self) != len(other): raise ValueError("Dimensiones incompatibles")
        return sum(a*b for a,b in zip(self.values, other.values))

    def norm(self): return sqrt(self.dot(self))
