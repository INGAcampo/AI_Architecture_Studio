from design.steel.column_domain import SteelColumnDesignResult
from design.steel.effective_length import EffectiveLengthEngine
from design.steel.column_slenderness import ColumnSlendernessEngine
from design.steel.compression_buckling import CompressionBucklingEngine
from design.steel.column_interaction import ColumnInteractionEngine

class SteelColumnDesignEngine:
    def __init__(self):
        self.effective=EffectiveLengthEngine()
        self.slenderness=ColumnSlendernessEngine()
        self.buckling=CompressionBucklingEngine()
        self.interaction=ColumnInteractionEngine()

    def design(self,column,profile,material):
        km=self.effective.factor(column.end_condition_major,column.k_major)
        kn=self.effective.factor(column.end_condition_minor,column.k_minor)
        em=column.length*km
        en=column.length*kn
        slender=self.slenderness.calculate(em,en,profile)
        buckling=self.buckling.calculate(profile,material,slender.maximum)
        major_capacity=material.fy*profile.zx
        minor_capacity=material.fy*profile.zy
        interaction=self.interaction.calculate(
            column.demand.axial,buckling.design_capacity,
            column.demand.moment_major,major_capacity,
            column.demand.moment_minor,minor_capacity,
        )
        checks={
            "axial":interaction.axial_ratio,
            "major_bending":interaction.major_ratio,
            "minor_bending":interaction.minor_ratio,
            "interaction":interaction.interaction_ratio,
        }
        governing=max(checks,key=checks.get)
        unity=checks[governing]
        return SteelColumnDesignResult(
            column.member_id,slender.major,slender.minor,slender.critical_axis,
            buckling.design_capacity,interaction.axial_ratio,interaction.major_ratio,
            interaction.minor_ratio,interaction.interaction_ratio,unity,unity<=1.0,governing
        )
