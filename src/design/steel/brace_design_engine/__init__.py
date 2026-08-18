from design.steel.brace_domain import BraceBehavior,SteelBraceDesignResult
from design.steel.brace_slenderness import BraceSlendernessEngine
from design.steel.brace_tension import BraceTensionEngine
from design.steel.brace_compression import BraceCompressionEngine

class SteelBraceDesignEngine:
    def __init__(self):
        self.slenderness=BraceSlendernessEngine()
        self.tension=BraceTensionEngine()
        self.compression=BraceCompressionEngine()

    def design(self,brace,profile,material):
        slender=self.slenderness.calculate(brace,profile)
        tension=self.tension.calculate(profile,material)
        compression=self.compression.calculate(profile,material,slender.slenderness)
        demand=brace.demand.axial
        tension_ratio=0.0
        compression_ratio=0.0
        if demand>=0 and brace.behavior is not BraceBehavior.COMPRESSION_ONLY:
            tension_ratio=abs(demand)/max(tension.design_capacity,1e-12)
        if demand<0 and brace.behavior is not BraceBehavior.TENSION_ONLY:
            compression_ratio=abs(demand)/max(compression.design_capacity,1e-12)
        if demand>=0 and brace.behavior is BraceBehavior.COMPRESSION_ONLY:
            tension_ratio=float("inf")
        if demand<0 and brace.behavior is BraceBehavior.TENSION_ONLY:
            compression_ratio=float("inf")
        checks={"tension":tension_ratio,"compression":compression_ratio,"slenderness":0.0 if slender.acceptable else slender.slenderness/200.0}
        governing=max(checks,key=checks.get)
        unity=checks[governing]
        return SteelBraceDesignResult(brace.member_id,tension.design_capacity,compression.design_capacity,slender.slenderness,tension_ratio,compression_ratio,unity,unity<=1.0,governing)
