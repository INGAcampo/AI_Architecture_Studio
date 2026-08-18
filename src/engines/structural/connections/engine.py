class SteelConnectionEngine:
    def __init__(self): self._items={}
    def add(self,c):
        if c.connection_id in self._items: raise KeyError(c.connection_id)
        self._items[c.connection_id]=c;return c
    def get(self,cid): return self._items[cid]
    def bolt_count(self,cid): return self.get(cid).bolts.count
    def plate_volume(self,cid,width,height): return width*height*self.get(cid).plate_thickness
