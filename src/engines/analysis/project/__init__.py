from dataclasses import dataclass, field

@dataclass(slots=True)
class AnalysisProject:
    project_id:str
    name:str
    nodes:dict = field(default_factory=dict)
    elements:dict = field(default_factory=dict)
    load_cases:dict = field(default_factory=dict)
    load_combinations:dict = field(default_factory=dict)
    settings:dict = field(default_factory=dict)

    def add_node(self,node): self.nodes[node.node_id]=node; return node
    def add_element(self,element): self.elements[element.element_id]=element; return element
    def add_load_case(self,case): self.load_cases[case.case_id]=case; return case
    def add_combination(self,combo): self.load_combinations[combo.combination_id]=combo; return combo

    def summary(self):
        return {
            "nodes":len(self.nodes),
            "elements":len(self.elements),
            "load_cases":len(self.load_cases),
            "load_combinations":len(self.load_combinations),
        }
