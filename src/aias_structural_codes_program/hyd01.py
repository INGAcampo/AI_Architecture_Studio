"""HYD-01 governed whole-network checks for water, sanitary and stormwater systems."""
from __future__ import annotations

from dataclasses import dataclass
import math
from .mdp02 import EngineeringStudyContext


@dataclass(frozen=True,slots=True)
class HydraulicNode:
    node_id:str;external_inflow_m3_s:float;demand_m3_s:float;elevation_m:float;source_id:str


@dataclass(frozen=True,slots=True)
class HydraulicLink:
    link_id:str;from_node:str;to_node:str;flow_m3_s:float;capacity_m3_s:float;area_m2:float;source_id:str


@dataclass(frozen=True,slots=True)
class HydraulicNetwork:
    network_id:str;network_type:str;context:EngineeringStudyContext;nodes:tuple[HydraulicNode,...];links:tuple[HydraulicLink,...];continuity_tolerance_m3_s:float;minimum_velocity_m_s:float;maximum_velocity_m_s:float
    def validate(self)->list[str]:
        issues=self.context.validate();known={x.source_id for x in self.context.sources}
        if not self.network_id:issues.append("network_id_required")
        if self.network_type not in {"WATER","SANITARY","STORMWATER"}:issues.append("unsupported_network_type")
        node_ids=[x.node_id for x in self.nodes];link_ids=[x.link_id for x in self.links]
        if len(node_ids)!=len(set(node_ids)):issues.append("duplicate_hydraulic_node")
        if len(link_ids)!=len(set(link_ids)):issues.append("duplicate_hydraulic_link")
        if not self.nodes or not self.links:issues.append("network_topology_incomplete")
        if self.continuity_tolerance_m3_s<0 or self.minimum_velocity_m_s<0 or self.maximum_velocity_m_s<=self.minimum_velocity_m_s:issues.append("invalid_network_limits")
        node_set=set(node_ids)
        for row in self.nodes:
            if not row.node_id or min(row.external_inflow_m3_s,row.demand_m3_s)<0 or not math.isfinite(row.elevation_m):issues.append(f"{row.node_id}:invalid_node")
            if row.source_id not in known:issues.append(f"{row.node_id}:unknown_source_id")
        for row in self.links:
            if not row.link_id or row.from_node not in node_set or row.to_node not in node_set:issues.append(f"{row.link_id}:invalid_connectivity")
            if min(row.flow_m3_s,row.capacity_m3_s,row.area_m2)<=0:issues.append(f"{row.link_id}:invalid_link_properties")
            if row.source_id not in known:issues.append(f"{row.link_id}:unknown_source_id")
        return issues


@dataclass(frozen=True,slots=True)
class NodeContinuity:
    node_id:str;inflow_m3_s:float;outflow_m3_s:float;demand_m3_s:float;residual_m3_s:float;status:str


@dataclass(frozen=True,slots=True)
class LinkCheck:
    link_id:str;velocity_m_s:float;capacity_utilization:float;status:str


@dataclass(frozen=True,slots=True)
class HydraulicNetworkResult:
    network_id:str;status:str;nodes:tuple[NodeContinuity,...];links:tuple[LinkCheck,...];maximum_continuity_residual_m3_s:float;maximum_capacity_utilization:float;issues:tuple[str,...];normative_compliance_claimed:bool;construction_approved:bool=False


class HydraulicNetworkEngine:
    def evaluate(self,network:HydraulicNetwork)->HydraulicNetworkResult:
        issues=network.validate();node_checks=[];link_checks=[];max_residual=max_utilization=0.0
        for node in network.nodes:
            incoming=sum(x.flow_m3_s for x in network.links if x.to_node==node.node_id);outgoing=sum(x.flow_m3_s for x in network.links if x.from_node==node.node_id)
            residual=node.external_inflow_m3_s+incoming-outgoing-node.demand_m3_s;max_residual=max(max_residual,abs(residual));status="PASS" if abs(residual)<=network.continuity_tolerance_m3_s else "FAIL"
            if status=="FAIL":issues.append(f"{node.node_id}:continuity_failure")
            node_checks.append(NodeContinuity(node.node_id,node.external_inflow_m3_s+incoming,outgoing,node.demand_m3_s,residual,status))
        for link in network.links:
            if link.area_m2<=0 or link.capacity_m3_s<=0:continue
            velocity=link.flow_m3_s/link.area_m2;utilization=link.flow_m3_s/link.capacity_m3_s;max_utilization=max(max_utilization,utilization)
            failures=[]
            if utilization>1:failures.append("capacity")
            if not network.minimum_velocity_m_s<=velocity<=network.maximum_velocity_m_s:failures.append("velocity")
            if failures:issues.append(f"{link.link_id}:{'_and_'.join(failures)}_failure")
            link_checks.append(LinkCheck(link.link_id,velocity,utilization,"PASS" if not failures else "FAIL"))
        normative=not issues and network.context.normative_claim_allowed()
        return HydraulicNetworkResult(network.network_id,"PASS_NORMATIVE_REVIEW_REQUIRED" if normative else ("PASS_REFERENCE" if not issues else "REJECTED"),tuple(node_checks),tuple(link_checks),max_residual,max_utilization,tuple(issues),normative,False)
