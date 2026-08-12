from PySide6.QtCore import Qt
from commands.base_command import BaseCommand
from core.history.add_window_action import AddWindowAction
from engines.architectural.opening_engine import OpeningEngine
from engines.architectural.window_engine import WindowEngine
from engines.geometry.point import Point
from models.architectural.window import Window
class WindowCommand(BaseCommand):
    PICK_TOLERANCE=.75
    def __init__(self,app_core=None):
        super().__init__(app_core);self.name='WINDOW';self.width=1.2;self.height=1.0;self.sill_height=.9;self.window_type=Window.SLIDING;self.selected_wall=None;self.awaiting_property=None
    def _window(self,c):
        g=getattr(c,'window',None);return g() if callable(g) else None
    def _status(self,c,t):
        w=self._window(c)
        if w:w.statusBar().showMessage(t)
    def _prompt(self,c,t):
        w=self._window(c);cl=getattr(w,'command_line',None)
        if cl:cl.set_prompt(t);cl.focus_input()
    def _scene(self,c):return getattr(self.app_core,'scene',getattr(c,'scene',None))
    def _point(self,c):
        g=getattr(c,'get_input_point',None)
        if callable(g):return g()
        x,y=c.cursor_position;return Point(x,y,0)
    def _walls(self,s):
        g=getattr(s,'get_elements',None);es=g() if callable(g) else []
        return [e for e in es if e.__class__.__name__=='Wall' and getattr(e,'visible',True)]
    def begin(self,c):
        self.selected_wall=None;print(f'WINDOW activado: A={self.width:g}, H={self.height:g}, AP={self.sill_height:g}, tipo={self.window_type}');self._prompt(c,'Seleccione muro para WINDOW:')
    def mouse_press(self,event,c):
        s=self._scene(c);p=self._point(c)
        if self.selected_wall is None:
            r=OpeningEngine.nearest_wall(self._walls(s),p,tolerance=self.PICK_TOLERANCE)
            if r is None:self._status(c,'WINDOW: no se encontró muro');return
            self.selected_wall=r['wall'];c.highlight.set(self.selected_wall);c.update();self._prompt(c,'Indique centro de ventana:');return
        win=WindowEngine.create_window(self.selected_wall,p,self.width,self.height,self.sill_height,self.window_type);WindowEngine.add_to_wall(self.selected_wall,win)
        if self.app_core is not None:self.app_core.history.push(AddWindowAction(s,self.selected_wall,win))
        s.wall_network_signature=None;print(f'WINDOW creada: ancho={win.width:g} m, altura={win.height:g} m, antepecho={win.sill_height:g} m, tipo={win.window_type}')
        self.selected_wall=None;c.highlight.clear();c.update();self._prompt(c,'Seleccione otro muro o ESC:')
    def handle_text_input(self,text,c):
        v=str(text or '').strip();u=v.upper()
        if self.awaiting_property:
            try:n=float(v.replace(',','.'))
            except ValueError:return True
            if self.awaiting_property=='width':self.width=n
            elif self.awaiting_property=='height':self.height=n
            else:self.sill_height=n
            self.awaiting_property=None;return True
        if u in ('A','ANCHO'):self.awaiting_property='width';self._prompt(c,'Ancho:');return True
        if u in ('H','ALTURA'):self.awaiting_property='height';self._prompt(c,'Altura:');return True
        if u in ('AP','ANTEPECHO'):self.awaiting_property='sill';self._prompt(c,'Antepecho:');return True
        if u in ('C','CORREDIZA'):self.window_type=Window.SLIDING;return True
        if u in ('AB','ABATIBLE'):self.window_type=Window.CASEMENT;return True
        return False
    def key_press(self,event,c):
        if event.key()==Qt.Key_Escape:self.cancel(c)
    def cancel(self,c=None):
        self.selected_wall=None
        if c:c.highlight.clear();c.update()
        print('WINDOW cancelado')
