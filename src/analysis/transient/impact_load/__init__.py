class Engine:
    def calculate(self,*values):
        return sum(float(v) for v in values if isinstance(v,(int,float)))
