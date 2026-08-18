class Engine:
    def calculate(self,*v): return sum(float(x) for x in v if isinstance(x,(int,float)))
