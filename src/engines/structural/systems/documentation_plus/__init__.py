from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class StructuralReport:
    report_id:str
    title:str
    rows:tuple[tuple,...]
    summary:dict

class StructuralDocumentationPlus:
    def load_report(self,load_cases,combinations):
        rows=tuple((c.case_id,c.name,c.category.value,c.self_weight_multiplier) for c in sorted(load_cases,key=lambda x:x.case_id))
        return StructuralReport("loads","Load Report",rows,{"cases":len(load_cases),"combinations":len(combinations)})
    def foundation_report(self,foundations,engine):
        rows=tuple((f.foundation_id,f.kind.value,engine.quantities(f).area,engine.quantities(f).volume) for f in sorted(foundations,key=lambda x:x.foundation_id))
        return StructuralReport("foundations","Foundation Report",rows,{"count":len(foundations)})
