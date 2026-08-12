class ElementDofMapper:
    def map(self,mgr,nodes,components): return tuple(mgr.index(n,c) for n in nodes for c in components)
