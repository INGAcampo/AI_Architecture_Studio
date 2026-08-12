class SectionSelector:
    def lightest_passing(self, candidates):
        passing=[x for x in candidates if x["status"]=="PASS"]
        return min(passing,key=lambda x:x["mass_kg_m"]) if passing else None
