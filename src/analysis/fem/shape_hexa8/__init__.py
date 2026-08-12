class ShapeHexa8:
 SIGNS=((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))
 def evaluate(self,x,e,z): return tuple(.125*(1+a*x)*(1+b*e)*(1+c*z) for a,b,c in self.SIGNS)
