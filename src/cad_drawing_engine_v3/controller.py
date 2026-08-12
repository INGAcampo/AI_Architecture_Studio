from cad_professional_kernel.geometry import Point2D
from .commands import LineCommand,CircleCommand,PolylineCommand
from .input_model import DynamicInput
from .rubber_band import RubberBand

class DrawingController:
    def __init__(self,kernel):
        self.kernel=kernel
        self.active=None
        self.dynamic=DynamicInput()
        self.rubber=RubberBand()
        self.preview_entity=None

    def start(self,name):
        name=name.upper()
        mapping={"LINE":LineCommand,"CIRCLE":CircleCommand,"POLYLINE":PolylineCommand}
        if name not in mapping: raise KeyError(name)
        self.active=mapping[name]()
        self.dynamic.prompt=self.active.prompt
        self.preview_entity=None
        return self.active

    def click(self,point):
        if not self.active: return None
        result=self.active.click(point)
        self.dynamic.prompt=self.active.prompt
        if getattr(self.active,"first",None) is not None:
            self.rubber.start(getattr(self.active,"first"))
        if getattr(self.active,"center",None) is not None:
            self.rubber.start(getattr(self.active,"center"))
        if result is not None:
            self.kernel.add(result)
            self.cancel()
            return result
        return None

    def move(self,point):
        if not self.active: return None
        self.preview_entity=self.active.preview(point)
        self.rubber.update(point)
        return self.preview_entity

    def finish_polyline(self,closed=False):
        if not isinstance(self.active,PolylineCommand): return None
        result=self.active.finish(closed)
        if result:
            self.kernel.add(result)
            self.cancel()
        return result

    def cancel(self):
        self.active=None
        self.dynamic.clear()
        self.rubber.stop()
        self.preview_entity=None
