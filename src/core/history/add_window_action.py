from engines.architectural.window_engine import WindowEngine
class AddWindowAction:
    def __init__(self,scene,wall,window):
        self.scene=scene;self.wall=wall;self.window=window;self.window_id=window.window_id;self.opening=window.opening;self.is_applied=True
    def _invalidate(self):
        if self.scene is not None:self.scene.wall_network_signature=None
    def undo(self):
        if not self.is_applied:return False
        ok=WindowEngine.remove_from_wall(self.wall,self.window)
        if ok:self.is_applied=False;self._invalidate()
        return ok
    def redo(self):
        if self.is_applied:return False
        self.opening.attach_window(self.window);WindowEngine.add_to_wall(self.wall,self.window);self.is_applied=True;self._invalidate();return True
