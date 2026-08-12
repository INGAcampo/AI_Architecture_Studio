from analysis.rc_columns.rc_column_domain import RCColumnResult
from analysis.rc_columns.axial_capacity import AxialCapacityEngine
from analysis.rc_columns.uniaxial_flexure import UniaxialFlexureEngine
from analysis.rc_columns.pmm_interaction import PMMInteractionEngine
from analysis.rc_columns.column_section import ColumnSection
from analysis.rc_columns.slenderness_ratio import SlendernessRatioEngine
class ColumnDesignPipeline:
    def design(self,c):
        s=ColumnSection(c.width,c.depth);ag=s.area()
        pn=AxialCapacityEngine().design(AxialCapacityEngine().nominal(c.concrete_strength,ag,c.steel_area,c.steel_yield_strength))
        mnx=UniaxialFlexureEngine().capacity(pn,c.depth);mny=UniaxialFlexureEngine().capacity(pn,c.width)
        interaction=PMMInteractionEngine().ratio(c.axial_load,pn,c.moment_x,mnx,c.moment_y,mny)
        radius=SlendernessRatioEngine().radius_of_gyration(ag,min(s.inertia_x(),s.inertia_y()))
        slenderness=SlendernessRatioEngine().calculate(1,c.length,radius)
        return RCColumnResult(pn,mnx,mny,interaction,slenderness,"PASS" if interaction<=1 else "FAIL")
