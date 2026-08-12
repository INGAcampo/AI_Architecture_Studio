from analysis.gpu.gpu_domain import GPURunResult
class GPUConjugateGradientSolver:
    def solve(self,A,b,tol=1e-10,max_iterations=100):
        n=len(b);x=[0.0]*n
        def mv(v): return [sum(a*z for a,z in zip(r,v)) for r in A]
        r=[b[i]-mv(x)[i] for i in range(n)];p=r[:];rr=sum(v*v for v in r)
        for k in range(1,max_iterations+1):
            ap=mv(p);alpha=rr/max(sum(p[i]*ap[i] for i in range(n)),1e-12)
            x=[x[i]+alpha*p[i] for i in range(n)];r=[r[i]-alpha*ap[i] for i in range(n)]
            nr=sum(v*v for v in r)
            if nr**.5<=tol:return tuple(x),GPURunResult("simulated-gpu",k,nr**.5,True,0.0)
            beta=nr/max(rr,1e-12);p=[r[i]+beta*p[i] for i in range(n)];rr=nr
        return tuple(x),GPURunResult("simulated-gpu",max_iterations,rr**.5,False,0.0)
