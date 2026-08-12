import json
from pathlib import Path
import pytest
from aias_enterprise_knowledge_graph import Edge,EnterpriseKnowledgeGraph,InferenceRule,Node,RuleRegistry
from aias_enterprise_knowledge_graph.bootstrap import import_master_inventory
ROOT=Path(__file__).resolve().parents[1]
def node(i):return Node(i,"SYSTEM",i,provenance={"source":"test"})
def test_persistence_uniqueness_and_endpoint_integrity(tmp_path):
 g=EnterpriseKnowledgeGraph(tmp_path/"graph.json");g.add_node(node("A"));g.add_node(node("B"));g.add_edge(Edge("E1","A","enables","B",provenance={"source":"test"}));assert EnterpriseKnowledgeGraph(g.path).related("A","outgoing")[0]["target"]=="B"
 with pytest.raises(ValueError,match="unknown_endpoint"):g.add_edge(Edge("E2","A","enables","X",provenance={"source":"test"}))
 with pytest.raises(ValueError,match="node_id_conflict"):g.add_node(Node("A","OTHER","changed",provenance={"source":"test"}))
def test_path_and_transitive_impact(tmp_path):
 g=EnterpriseKnowledgeGraph(tmp_path/"g.json");[g.add_node(node(x)) for x in "ABC"]
 g.add_edge(Edge("AB","A","enables","B",provenance={"source":"test"}));g.add_edge(Edge("BC","B","enables","C",provenance={"source":"test"}));assert g.shortest_path("A","C")==["A","B","C"] and g.impact("A")==["B","C"]
def test_only_approved_rules_infer_with_provenance(tmp_path):
 rule=InferenceRule("R1","requires","produces","depends_on","AIAS-GOV");g=EnterpriseKnowledgeGraph(tmp_path/"g.json",RuleRegistry([rule]));[g.add_node(node(x)) for x in "ABC"]
 g.add_edge(Edge("AB","A","requires","B",provenance={"source":"test"}));g.add_edge(Edge("BC","B","produces","C",provenance={"source":"test"}));row=g.infer("R1")[0];assert row["provenance"]["rule_id"]=="R1" and row["target"]=="C"
 with pytest.raises(ValueError,match="unapproved"):g.infer("UNKNOWN")
def test_master_inventory_is_an_immediate_real_consumer(tmp_path):
 g=EnterpriseKnowledgeGraph(tmp_path/"enterprise.json");result=import_master_inventory(g,ROOT/"engineering/aias/master/inventory/AIAS_MASTER_CONCEPT_INVENTORY.json");assert result["nodes"]>=60 and "SYS-000006" in g.data["nodes"] and len(g.impact("FOUND-000004"))>0
