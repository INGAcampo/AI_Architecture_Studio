class TsaiWuEngine:
    def index(self,s1,s2,t12,xt,xc,yt,yc,s): return (1/xt-1/xc)*s1+(1/yt-1/yc)*s2+s1*s1/(xt*xc)+s2*s2/(yt*yc)+t12*t12/(s*s)
