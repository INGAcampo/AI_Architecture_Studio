class JacobiPreconditioner:
    def build(self,A):return tuple(1/max(abs(A[i][i]),1e-12) for i in range(len(A)))
