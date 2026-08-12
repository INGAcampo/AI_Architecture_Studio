from engines.fem.truss import TrussElement
from engines.fem.beam import BeamElement2D
from engines.fem.frame import FrameElement2D
from engines.fem.plate import PlateElement4
from engines.fem.shell import ShellElement4

class FiniteElementFactory:
    def create(self,element_type,**kwargs):
        mapping={
            "truss":TrussElement,
            "beam2d":BeamElement2D,
            "frame2d":FrameElement2D,
            "plate4":PlateElement4,
            "shell4":ShellElement4,
        }
        if element_type not in mapping: raise KeyError(element_type)
        return mapping[element_type](**kwargs)
