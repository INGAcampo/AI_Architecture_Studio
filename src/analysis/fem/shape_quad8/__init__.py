class ShapeQuad8:
 def evaluate(self,x,e): return (-.25*(1-x)*(1-e)*(1+x+e),-.25*(1+x)*(1-e)*(1-x+e),-.25*(1+x)*(1+e)*(1-x-e),-.25*(1-x)*(1+e)*(1+x-e),.5*(1-x*x)*(1-e),.5*(1+x)*(1-e*e),.5*(1-x*x)*(1+e),.5*(1-x)*(1-e*e))
