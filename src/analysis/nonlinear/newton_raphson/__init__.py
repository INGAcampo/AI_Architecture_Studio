class NewtonRaphsonSolver:
 def solve(self,f,df,x0,tol=1e-8,max_iterations=50):
  x=float(x0)
  for i in range(max_iterations):
   r=f(x)
   if abs(r)<=tol:return x,i+1,True
   t=df(x)
   if abs(t)<1e-12:break
   x-=r/t
  return x,max_iterations,False
