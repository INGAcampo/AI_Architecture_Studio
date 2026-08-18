from dataclasses import dataclass,field

@dataclass(slots=True)
class StructuralResultsDatabase:
    node_results:dict = field(default_factory=dict)
    element_results:dict = field(default_factory=dict)
    metadata:dict = field(default_factory=dict)

    def store_node_result(self,case_id,node_id,result):
        self.node_results[(case_id,node_id)]=result

    def store_element_result(self,case_id,element_id,result):
        self.element_results[(case_id,element_id)]=result

    def get_node_result(self,case_id,node_id):
        return self.node_results[(case_id,node_id)]

    def get_element_result(self,case_id,element_id):
        return self.element_results[(case_id,element_id)]

    def cases(self):
        return tuple(sorted({k[0] for k in self.node_results}|{k[0] for k in self.element_results}))
