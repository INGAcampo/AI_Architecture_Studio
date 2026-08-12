class SectionSearchEngine:
    def by_designation(self,sections,d): return next((s for s in sections if s.designation.upper()==d.upper()),None)
