from analysis.steel_library.steel_material_domain import SteelMaterial
from analysis.steel_library.section_domain import SteelSection
from analysis.steel_library.section_validation import SectionValidationEngine
class SteelLibraryPipeline:
    def build_demo(self):
        m=SteelMaterial("ASTM A992","ASTM",345.,450.)
        s=SteelSection("W14X38","W",7210.,56.5,3.85e8,1.32e7,4.2e5,1.15e12,358.,171.)
        return m,s,SectionValidationEngine().validate(s)
