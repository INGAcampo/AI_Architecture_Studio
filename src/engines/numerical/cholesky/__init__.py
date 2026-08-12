from dataclasses import dataclass
from math import sqrt
from engines.numerical.vectors import DenseVector

@dataclass(frozen=True, slots=True)
class CholeskyFactor:
    lower:tuple[tuple[float,...],...]

class CholeskyEngine:
    def factor(self,matrix):
        a=matrix.rows; n=len(a); l=[[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1):
                s=sum(l[i][k]*l[j][k] for k in range(j))
                if i==j:
                    value=a[i][i]-s
                    if value<=0: raise ValueError("Matriz no definida positiva")
                    l[i][j]=sqrt(value)
                else:
                    l[i][j]=(a[i][j]-s)/l[j][j]
        return CholeskyFactor(tuple(tuple(r) for r in l))

    def solve(self,matrix,vector):
        l=self.factor(matrix).lower; n=len(vector)
        y=[0.0]*n
        for i in range(n): y[i]=(vector[i]-sum(l[i][j]*y[j] for j in range(i)))/l[i][i]
        x=[0.0]*n
        for i in range(n-1,-1,-1): x[i]=(y[i]-sum(l[j][i]*x[j] for j in range(i+1,n)))/l[i][i]
        return DenseVector(tuple(x))
