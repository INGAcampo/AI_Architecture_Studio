from dataclasses import dataclass
from analysis.steel_library.steel_library_pipeline import SteelLibraryPipeline
from analysis.steel_library.section_report import SectionReportEngine
from analysis.steel_library.section_unit_conversion import SectionUnitConverter
@dataclass(frozen=True,slots=True)
class WorkflowResult: material:object; section:object; validation:object; area_in2:float; mass_lb_ft:float; report:str
class SteelLibraryVerticalSlice:
    def run(self):
        m,s,v=SteelLibraryPipeline().build_demo(); c=SectionUnitConverter()
        return WorkflowResult(m,s,v,c.mm2_to_in2(s.area_mm2),c.kg_m_to_lb_ft(s.mass_kg_m),SectionReportEngine().build(m,s))
