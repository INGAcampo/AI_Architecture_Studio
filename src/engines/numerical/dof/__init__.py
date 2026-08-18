from dataclasses import dataclass

DOF_NAMES=("ux","uy","uz","rx","ry","rz")

@dataclass(frozen=True, slots=True)
class DofMap:
    equation_by_node_dof:dict[tuple[str,str],int|None]
    free_count:int
    restrained_count:int

class GlobalDofManager:
    def build(self,nodes):
        mapping={}; free=0; restrained=0
        for node in sorted(nodes,key=lambda n:n.node_id):
            for name in DOF_NAMES:
                fixed=getattr(node.restraint,name)
                if fixed:
                    mapping[(node.node_id,name)]=None; restrained+=1
                else:
                    mapping[(node.node_id,name)]=free; free+=1
        return DofMap(mapping,free,restrained)

    def member_equations(self,dof_map,start_node_id,end_node_id):
        return tuple(dof_map.equation_by_node_dof[(nid,d)] for nid in (start_node_id,end_node_id) for d in DOF_NAMES)
