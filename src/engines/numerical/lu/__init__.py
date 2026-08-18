from dataclasses import dataclass
from engines.numerical.vectors import DenseVector

@dataclass(frozen=True, slots=True)
class LUFactorization:
    lower:tuple[tuple[float,...],...]
    upper:tuple[tuple[float,...],...]

class LUFactorizationEngine:
    def factor(self,matrix):
        a=[list(r) for r in matrix.rows]; n=len(a)
        l=[[0.0]*n for _ in range(n)]; u=[[0.0]*n for _ in range(n)]
        for i in range(n):
            for k in range(i,n):
                u[i][k]=a[i][k]-sum(l[i][j]*u[j][k] for j in range(i))
            if abs(u[i][i])<1e-15: raise ValueError("Matriz singular")
            l[i][i]=1.0
            for k in range(i+1,n):
                l[k][i]=(a[k][i]-sum(l[k][j]*u[j][i] for j in range(i)))/u[i][i]
        return LUFactorization(tuple(tuple(r) for r in l),tuple(tuple(r) for r in u))

    def solve(self,matrix,vector):
        f=self.factor(matrix); n=len(vector)
        y=[0.0]*n
        for i in range(n): y[i]=vector[i]-sum(f.lower[i][j]*y[j] for j in range(i))
        x=[0.0]*n
        for i in range(n-1,-1,-1):
            x[i]=(y[i]-sum(f.upper[i][j]*x[j] for j in range(i+1,n)))/f.upper[i][i]
        return DenseVector(tuple(x))
