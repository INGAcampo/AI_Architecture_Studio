class LaminateResultantsEngine:
    def calculate(self,A,B,D,e,k):
        n=tuple(sum(A[i][j]*e[j]+B[i][j]*k[j] for j in range(3)) for i in range(3)); m=tuple(sum(B[i][j]*e[j]+D[i][j]*k[j] for j in range(3)) for i in range(3)); return n,m
