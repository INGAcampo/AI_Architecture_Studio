from uuid import uuid4
class Window:
    SLIDING='sliding'; CASEMENT='casement'
    def __init__(self,opening=None,width=1.20,height=1.00,sill_height=0.90,window_type=SLIDING,name='Ventana',window_id=None):
        self.window_id=str(window_id or uuid4()); self.opening=opening
        self.width=float(width); self.height=float(height); self.sill_height=float(sill_height)
        self.window_type=str(window_type); self.name=str(name); self.visible=True
        if self.width<=0 or self.height<=0 or self.sill_height<0: raise ValueError('Dimensiones WINDOW inválidas.')
    @property
    def id(self): return self.window_id
    @property
    def host_wall(self): return self.opening.host_wall if self.opening else None
    @property
    def center_point(self): return self.opening.center_point if self.opening else None
    def clone(self,opening=None,preserve_id=False):
        return Window(opening if opening is not None else self.opening,self.width,self.height,self.sill_height,self.window_type,self.name,self.window_id if preserve_id else None)
