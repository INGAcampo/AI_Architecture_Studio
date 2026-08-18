from design.steel.bolt_domain import BoltConnectionType,BoltDesignResult
from design.steel.bolt_shear import BoltShearEngine
from design.steel.bolt_tension import BoltTensionEngine
from design.steel.plate_bearing import PlateBearingEngine
from design.steel.slip_critical import SlipCriticalEngine
from design.steel.bolt_interaction import BoltInteractionEngine

class BoltDesignEngine:
    def __init__(self):
        self.shear=BoltShearEngine()
        self.tension=BoltTensionEngine()
        self.bearing=PlateBearingEngine()
        self.slip=SlipCriticalEngine()
        self.interaction=BoltInteractionEngine()

    def design(self,bolt,demand,plate_thickness,plate_fu,edge_distance,spacing,shear_planes=1,pretension=125e3):
        shear=self.shear.calculate(bolt,shear_planes)
        tension=self.tension.calculate(bolt)
        bearing=self.bearing.calculate(bolt.diameter,plate_thickness,plate_fu,edge_distance,spacing)
        slip=self.slip.calculate(pretension)
        shear_capacity=min(shear.design_capacity,bearing.design_capacity)
        if bolt.connection_type is BoltConnectionType.SLIP_CRITICAL:
            shear_capacity=min(shear_capacity,slip.design_capacity)
        interaction=self.interaction.calculate(
            (demand.shear_x**2+demand.shear_y**2)**0.5,
            shear_capacity,
            demand.tension,
            tension.design_capacity,
        )
        checks={
            "shear":interaction.shear_ratio,
            "tension":interaction.tension_ratio,
            "interaction":interaction.interaction_ratio,
        }
        governing=max(checks,key=checks.get)
        unity=checks[governing]
        return BoltDesignResult(
            bolt.bolt_id,shear.design_capacity,tension.design_capacity,
            bearing.design_capacity,slip.design_capacity,
            interaction.shear_ratio,interaction.tension_ratio,
            interaction.interaction_ratio,unity,unity<=1.0,governing
        )
