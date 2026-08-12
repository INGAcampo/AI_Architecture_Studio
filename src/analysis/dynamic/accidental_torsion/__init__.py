class Engine:
    def calculate(self,*values):
        nums=[float(v) for v in values if isinstance(v,(int,float))]
        return sum(nums)
