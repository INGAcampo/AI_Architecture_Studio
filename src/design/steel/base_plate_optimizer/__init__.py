from dataclasses import dataclass,replace

@dataclass(frozen=True,slots=True)
class BasePlateOptimizationResult:
    original_dimensions:tuple
    recommended_dimensions:tuple|None
    maximum_unity:float|None
    steel_reduction_percent:float

class BasePlateOptimizer:
    def __init__(self,engine): self.engine=engine
    def optimize(
        self,plate,column,anchors,demand,fc,supporting_area,
        widths=(.35,.40,.45,.50,.55,.60,.65,.70),
        thicknesses=(.016,.020,.025,.030,.035,.040,.050,.060),
    ):
        feasible=[]
        for width in widths:
            for thickness in thicknesses:
                candidate=replace(plate,width=width,length=width,thickness=thickness)
                result=self.engine.design(candidate,column,anchors,demand,fc,supporting_area)
                if result.passed:
                    feasible.append((
                        width*width*thickness,
                        result.maximum_unity,
                        width,width,thickness,
                    ))
        if not feasible:
            return BasePlateOptimizationResult(
                (plate.width,plate.length,plate.thickness),
                None,None,0.0,
            )
        volume,unity,width,length,thickness=min(feasible)
        original=plate.width*plate.length*plate.thickness
        reduction=max(0.0,(original-volume)/original*100.0)
        return BasePlateOptimizationResult(
            (plate.width,plate.length,plate.thickness),
            (width,length,thickness),
            unity,reduction,
        )
