class CompositeDamageEvolution:
    def linear(self,x,onset,ultimate):
        if x<=onset:return 0.0
        if x>=ultimate:return .999999
        return (x-onset)/max(ultimate-onset,1e-12)
