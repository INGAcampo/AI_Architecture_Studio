from dataclasses import dataclass
from engines.numerical.vectors import DenseVector

@dataclass(frozen=True, slots=True)
class DenseMatrix:
    rows: tuple[tuple[float,...],...]

    def __post_init__(self):
        rows=tuple(tuple(float(v) for v in row) for row in self.rows)
        if not rows or not rows[0] or any(len(r)!=len(rows[0]) for r in rows):
            raise ValueError("Matriz inválida")
        object.__setattr__(self,"rows",rows)

    @property
    def shape(self): return (len(self.rows),len(self.rows[0]))
    def transpose(self):
        r,c=self.shape
        return DenseMatrix(tuple(tuple(self.rows[i][j] for i in range(r)) for j in range(c)))
    def matvec(self,vector):
        if self.shape[1]!=len(vector): raise ValueError("Dimensiones incompatibles")
        return DenseVector(tuple(sum(a*b for a,b in zip(row,vector.values)) for row in self.rows))
    def add(self,other):
        if self.shape!=other.shape: raise ValueError("Dimensiones incompatibles")
        return DenseMatrix(tuple(tuple(a+b for a,b in zip(ra,rb)) for ra,rb in zip(self.rows,other.rows)))
    @staticmethod
    def identity(n):
        return DenseMatrix(tuple(tuple(1.0 if i==j else 0.0 for j in range(n)) for i in range(n)))
