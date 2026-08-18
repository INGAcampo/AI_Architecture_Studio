from aias_structural_codes_program import EngineeringStudyContext,HydraulicLink,HydraulicNetwork,HydraulicNetworkEngine,HydraulicNode,StudySource


def context(status="REFERENCE",pack="",review="PENDING"):
    return EngineeringStudyContext("HYD","R00","BO","SI",(StudySource("H1","HYDRAULIC_MODEL","Lab","evidence://hyd",status),),pack,review)


def network(ctx=None,flow=.01,capacity=.02):
    nodes=(HydraulicNode("SOURCE",flow,0,100,"H1"),HydraulicNode("USER",0,flow,90,"H1"));links=(HydraulicLink("P1","SOURCE","USER",flow,capacity,.01,"H1"),)
    return HydraulicNetwork("NET-1","WATER",ctx or context(),nodes,links,.000001,.3,3)


def test_complete_network_passes_continuity_capacity_and_velocity():
    result=HydraulicNetworkEngine().evaluate(network())
    assert result.status=="PASS_REFERENCE" and result.issues==()
    assert result.maximum_continuity_residual_m3_s==0
    assert result.maximum_capacity_utilization==.5
    assert result.links[0].velocity_m_s==1
    assert result.construction_approved is False


def test_node_continuity_failure_is_rejected():
    item=network();nodes=(item.nodes[0],HydraulicNode("USER",0,.02,90,"H1"));item=HydraulicNetwork(item.network_id,item.network_type,item.context,nodes,item.links,item.continuity_tolerance_m3_s,item.minimum_velocity_m_s,item.maximum_velocity_m_s)
    result=HydraulicNetworkEngine().evaluate(item)
    assert result.status=="REJECTED"
    assert "USER:continuity_failure" in result.issues


def test_capacity_and_velocity_failures_are_reported():
    result=HydraulicNetworkEngine().evaluate(network(flow=.04,capacity=.02))
    assert result.status=="REJECTED"
    assert "P1:capacity_and_velocity_failure" in result.issues


def test_invalid_connectivity_and_unknown_source_fail_closed():
    item=network();links=(HydraulicLink("P","SOURCE","MISSING",.01,.02,.01,"UNKNOWN"),);item=HydraulicNetwork(item.network_id,item.network_type,item.context,item.nodes,links,item.continuity_tolerance_m3_s,item.minimum_velocity_m_s,item.maximum_velocity_m_s)
    issues=HydraulicNetworkEngine().evaluate(item).issues
    assert "P:invalid_connectivity" in issues
    assert "P:unknown_source_id" in issues


def test_authorized_network_still_requires_professional_release():
    result=HydraulicNetworkEngine().evaluate(network(context("AUTHORIZED","BO-HYD-001","ACCEPTED")))
    assert result.status=="PASS_NORMATIVE_REVIEW_REQUIRED"
    assert result.normative_compliance_claimed is True
    assert result.construction_approved is False
