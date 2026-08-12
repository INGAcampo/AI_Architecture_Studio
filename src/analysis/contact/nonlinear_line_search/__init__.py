class NonlinearLineSearchEngine:
    def backtrack(self,step,residual,max_iterations=12):
        base=abs(residual(0))
        for _ in range(max_iterations):
            if abs(residual(step))<base:return step
            step*=.5
        return step
