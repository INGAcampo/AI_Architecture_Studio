from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class StructuralRuleIssue:
    rule_id:str
    severity:str
    member_id:str
    message:str

class StructuralRuleEngine:
    def review_member(self,member,section_properties,material):
        issues=[]
        slenderness=member.length/min(section_properties.rx,section_properties.ry)
        if slenderness>200:
            issues.append(StructuralRuleIssue("member.slenderness","warning",member.member_id,f"λ={slenderness:.1f}"))
        if material.yield_strength<=0 and material.compressive_strength<=0:
            issues.append(StructuralRuleIssue("material.strength","error",member.member_id,"Material sin resistencia"))
        return tuple(issues)
