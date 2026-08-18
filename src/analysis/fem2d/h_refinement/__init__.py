class HRefinementEngine:
    def target_size(self,current,error,target): return current if error<=0 else current*(target/error)**.5