class SectionBimAdapter:
    def to_ifc_profile(self,s): return {"ProfileName":s.designation,"ProfileType":s.family,"Area":s.area_mm2}
