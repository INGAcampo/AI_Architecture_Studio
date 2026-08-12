from math import dist
from .matrix import axial_stiffness
class StructuralAnalysisCore:
    def __init__(self): self.nodes={}; self.elements={}
    def add_node(self,node):
        if node.node_id in self.nodes: raise KeyError(node.node_id)
        self.nodes[node.node_id]=node; return node
    def add_element(self,e):
        if e.element_id in self.elements: raise KeyError(e.element_id)
        if e.start_node_id not in self.nodes or e.end_node_id not in self.nodes: raise KeyError("Nodo faltante")
        self.elements[e.element_id]=e; return e
    def length(self,eid):
        e=self.elements[eid];a=self.nodes[e.start_node_id];b=self.nodes[e.end_node_id]
        return dist((a.x,a.y,a.z),(b.x,b.y,b.z))
    def stiffness(self,eid):
        e=self.elements[eid];return axial_stiffness(e.elastic_modulus,e.area,self.length(eid))
