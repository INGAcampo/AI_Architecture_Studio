class SectionFilterEngine:
    def minimum_area(self,sections,a): return tuple(s for s in sections if s.area_mm2>=a)
