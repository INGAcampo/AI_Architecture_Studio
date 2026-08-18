class ClosestPointEngine:
    def on_segment(self,p,a,b):
        ab=tuple(b[i]-a[i] for i in range(len(a)));ap=tuple(p[i]-a[i] for i in range(len(a)))
        t=max(0,min(1,sum(ap[i]*ab[i] for i in range(len(a)))/max(sum(v*v for v in ab),1e-12)))
        return tuple(a[i]+t*ab[i] for i in range(len(a)))
