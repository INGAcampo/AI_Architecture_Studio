class ConstraintManager:
    def apply(self,K,F,fixed):
        A=[list(r) for r in K];b=list(F)
        for d in fixed:
            for j in range(len(A)): A[d][j]=0;A[j][d]=0
            A[d][d]=1;b[d]=0
        return tuple(tuple(r) for r in A),tuple(b)
