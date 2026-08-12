from dataclasses import dataclass
from design.steel.base_plate_design_engine import BasePlateDesignEngine
from design.steel.base_plate_optimizer import BasePlateOptimizer
from design.steel.base_plate_report_ai import BasePlateReportAI
from design.steel.foundation_transfer import FoundationTransferEngine

@dataclass(frozen=True,slots=True)
class BasePlateWorkflowResult:
    design_result:object
    optimization_result:object
    transfer_result:object
    advice:object
    report:object

class BasePlateVerticalSlice:
    def run(self,plate,column,anchors,demand,fc,supporting_area):
        engine=BasePlateDesignEngine()
        design=engine.design(plate,column,anchors,demand,fc,supporting_area)
        optimization=BasePlateOptimizer(engine).optimize(plate,column,anchors,demand,fc,supporting_area)
        transfer=FoundationTransferEngine().calculate(demand,design)
        ai=BasePlateReportAI()
        return BasePlateWorkflowResult(design,optimization,transfer,ai.advise(design,optimization),ai.build(plate,design,optimization))
