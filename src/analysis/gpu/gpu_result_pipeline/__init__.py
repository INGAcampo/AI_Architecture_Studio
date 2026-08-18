class GPUResultPipeline:
    def normalize(self,v):
        lo=min(v);hi=max(v);span=max(hi-lo,1e-12)
        return tuple((x-lo)/span for x in v)
