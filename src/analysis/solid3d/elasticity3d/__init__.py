class Elasticity3DEngine:
    def matrix(self,E,nu):
        la=E*nu/((1+nu)*(1-2*nu));mu=E/(2*(1+nu));d=[[0.]*6 for _ in range(6)]
        for i in range(3):
            for j in range(3):d[i][j]=la
            d[i][i]+=2*mu
        for i in range(3,6):d[i][i]=mu
        return tuple(tuple(r) for r in d)
