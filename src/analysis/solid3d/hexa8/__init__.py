class Hexa8Engine:
    def shape(self,x,y,z):
        s=((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))
        return tuple(.125*(1+a*x)*(1+b*y)*(1+c*z) for a,b,c in s)
