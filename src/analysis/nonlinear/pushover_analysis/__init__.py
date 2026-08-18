from analysis.nonlinear.nonlinear_domain import NonlinearStep,NonlinearAnalysisResult
class PushoverAnalysisEngine:
 def run(self,k,fy,b,target,steps=20):
  out=[];peak=0.0;uy=fy/max(k,1e-12)
  for i in range(1,steps+1):
   u=target*i/steps;force=k*u if u<=uy else fy+k*b*(u-uy);lf=force/max(fy,1e-12);peak=max(peak,lf);out.append(NonlinearStep(i,lf,u,0.0,True))
  return NonlinearAnalysisResult(tuple(out),peak,target,True)
