"""Public module supporting AEPS repeatable generation and delivery automation."""
from dataclasses import dataclass,field
@dataclass(slots=True)
class DependencyGraph:
    """Execute the public DependencyGraph operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    edges:dict[str,set[str]]=field(default_factory=dict)
    def add_node(self,n):
        """Add an idempotent dependency-graph node."""
        self.edges.setdefault(n,set())
    def add_edge(self,s,t):
        """Add a directed dependency edge after ensuring both endpoint nodes."""
        self.add_node(s); self.add_node(t); self.edges[s].add(t)
    def dependencies_of(self,n):
        """Return direct dependencies of a node in deterministic order."""
        return tuple(sorted(self.edges.get(n,set())))
    def topological_order(self):
        """Execute the public DependencyGraph.topological_order operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
        indeg={n:0 for n in self.edges}
        for ts in self.edges.values():
            for t in ts: indeg[t]=indeg.get(t,0)+1
        q=sorted([n for n,d in indeg.items() if d==0]); out=[]
        while q:
            n=q.pop(0); out.append(n)
            for t in sorted(self.edges.get(n,set())):
                indeg[t]-=1
                if indeg[t]==0: q.append(t); q.sort()
        if len(out)!=len(indeg): raise ValueError('Dependency cycle detected')
        return tuple(out)
