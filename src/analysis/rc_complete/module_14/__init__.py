class Engine:
    def calculate(self,*v):return sum(float(x) for x in v if isinstance(x,(int,float)))
    def utilization(self,demand,capacity):return demand/max(capacity,1e-12)
