class AdaptiveMarkingEngine:
    def mark(self,errors,fraction=.3):
        count=max(1,int(len(errors)*fraction)); return tuple(i for i,_ in sorted(enumerate(errors),key=lambda x:x[1],reverse=True)[:count])