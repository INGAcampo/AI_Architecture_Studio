from analysis.hpc.hpc_domain import Partition
class DomainPartitionEngine:
    def partition(self,ids,workers):
        buckets=[[] for _ in range(max(1,workers))]
        for i,e in enumerate(ids):buckets[i%len(buckets)].append(e)
        return tuple(Partition(i,tuple(b),float(len(b))) for i,b in enumerate(buckets))
