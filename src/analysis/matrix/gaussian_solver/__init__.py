class GaussianSolver:
    def solve(self,A,b):
        a=[list(r)+[float(v)] for r,v in zip(A,b)];n=len(a)
        for i in range(n):
            p=max(range(i,n),key=lambda r:abs(a[r][i]));a[i],a[p]=a[p],a[i]
            q=a[i][i]
            if abs(q)<1e-12: raise ValueError("Singular")
            for j in range(i,n+1):a[i][j]/=q
            for r in range(n):
                if r==i:continue
                f=a[r][i]
                for j in range(i,n+1):a[r][j]-=f*a[i][j]
        return tuple(r[-1] for r in a)
