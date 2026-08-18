class TimeGridEngine:
    def build(self,start,end,dt):
        n=int(round((end-start)/dt))
        return tuple(start+i*dt for i in range(n+1))
