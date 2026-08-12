"""System optimization summary and consolidated structural report."""
from __future__ import annotations
from dataclasses import asdict
from .analysis import AnalysisRequest,AnalysisResult
from .design import BatchDesignResult,DesignRulePack

def consolidated_report(request:AnalysisRequest,analysis:AnalysisResult,design:BatchDesignResult,pack:DesignRulePack)->dict:
    """Join the complete structural workflow into one review-safe technical record."""
    issues=request.validate()+analysis.validate_against(request)+list(design.issues);capacities={(x.member_kind,x.section_id):x for x in pack.capacities};weights=[]
    nodes={x.node_id:x for x in request.building.nodes};members={x.member_id:x for x in request.building.members}
    for row in design.designs:
        cap=capacities.get((row.member_kind,row.selected_section_id));member=members.get(row.member_id)
        if cap and member:
            a,b=nodes[member.start_node],nodes[member.end_node];length=((a.x_m-b.x_m)**2+(a.y_m-b.y_m)**2+(a.z_m-b.z_m)**2)**.5;weights.append(cap.weight_kg_m*length)
    passing=sum(x.status=="PASS_REFERENCE" for x in design.designs);failing=len(design.designs)-passing;maximum=max((x.governing_ratio for x in design.designs),default=0)
    return {"report_id":f"REPORT-{request.analysis_id}","schema":"AIAS-STRUCTURAL-CONSOLIDATED-1.0","project_id":request.building.project_id,"building_id":request.building.building_id,"revision":request.building.revision,"analysis":{"id":analysis.analysis_id,"solver_id":analysis.solver_id,"solver_version":analysis.solver_version,"status":analysis.status,"load_cases":len(request.load_cases),"member_demands":len(analysis.demands)},"design":{"rule_pack_id":design.rule_pack_id,"rule_pack_version":design.rule_pack_version,"legal_status":design.legal_status,"members":len(design.designs),"passing_reference":passing,"requiring_action":failing,"maximum_utilization":maximum,"selected_sections":[asdict(x) for x in design.designs]},"optimization":{"objective":"minimum declared member weight among passing candidates","estimated_selected_weight_kg":sum(weights),"global_optimum_claimed":False},"issues":sorted(set(issues)),"status":"FOR_PROFESSIONAL_REVIEW" if not issues else "INCOMPLETE","normative_compliance_claimed":False,"construction_approved":False}
