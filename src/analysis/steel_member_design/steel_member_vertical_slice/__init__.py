from analysis.steel_member_design.member_model import SteelMember
from analysis.steel_member_design.member_demands import MemberDemands
from analysis.steel_member_design.member_capacity import MemberCapacity
from analysis.steel_member_design.member_unity_check import MemberUnityCheck
from analysis.steel_member_design.design_diagnostics import DesignDiagnostics
from analysis.steel_member_design.ai_design_advisor import AiDesignAdvisor
from analysis.steel_member_design.steel_member_report import SteelMemberReport

class SteelMemberVerticalSlice:
    def run(self):
        member=SteelMember("SM-DEMO-001",6.0,1.0,1.0,3.0)
        demands=MemberDemands(450000.0,120000000.0,20000000.0,85000.0,0.0)
        capacity=MemberCapacity(900000.0,220000000.0,80000000.0,180000.0)
        result=MemberUnityCheck().evaluate(demands,capacity)
        diagnostics=DesignDiagnostics().messages(result)
        advice=AiDesignAdvisor().advise(result)
        report=SteelMemberReport().build(member,result,"W14X38")
        return member,demands,capacity,result,diagnostics,advice,report
