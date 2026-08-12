class Tetra4Engine:
    def volume(self,c):
        a,b,d,e=c
        u=[b[i]-a[i] for i in range(3)];v=[d[i]-a[i] for i in range(3)];q=[e[i]-a[i] for i in range(3)]
        det=u[0]*(v[1]*q[2]-v[2]*q[1])-u[1]*(v[0]*q[2]-v[2]*q[0])+u[2]*(v[0]*q[1]-v[1]*q[0])
        return abs(det)/6
