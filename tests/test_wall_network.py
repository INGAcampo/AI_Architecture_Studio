"""Pruebas geométricas aisladas para WALL NETWORK 5.0.4.3."""

import importlib.util
import sys
import types
from pathlib import Path


class Point:
    def __init__(self, x, y, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_to(self, other):
        return ((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2) ** 0.5


class WallNode:
    ENDPOINT="ENDPOINT"; L_JOIN="L"; T_JOIN="T"; X_JOIN="X"; INTERSECTION="INTERSECTION"
    def __init__(self,node_id,position,node_type=ENDPOINT):
        self.node_id=str(node_id); self.position=Point(position.x,position.y,getattr(position,"z",0.0)); self.node_type=node_type; self.connections=[]
    def add_connection(self,wall,segment_index,parameter,endpoint=False):
        for item in self.connections:
            if item["wall"] is wall and item["segment_index"]==segment_index and abs(item["parameter"]-parameter)<=1e-9: return
        self.connections.append({"wall":wall,"segment_index":int(segment_index),"parameter":float(parameter),"endpoint":bool(endpoint)})
    @property
    def degree(self): return len(self.connections)
    @property
    def connected_walls(self):
        result=[]
        for item in self.connections:
            if item["wall"] not in result: result.append(item["wall"])
        return result
    def as_dict(self): return {"node_id":self.node_id}


point_module=types.ModuleType("engines.geometry.point"); point_module.Point=Point
node_module=types.ModuleType("models.architectural.wall_node"); node_module.WallNode=WallNode

# Load the module with temporary dependency doubles and restore the real
# package registry immediately afterwards.  Leaving these doubles in
# sys.modules polluted unrelated tests collected later in the same session.
_module_names = (
    "engines",
    "engines.geometry",
    "engines.geometry.point",
    "models",
    "models.architectural",
    "models.architectural.wall_node",
)
_previous_modules = {name: sys.modules.get(name) for name in _module_names}
try:
    sys.modules["engines"] = types.ModuleType("engines")
    sys.modules["engines.geometry"] = types.ModuleType("engines.geometry")
    sys.modules["engines.geometry.point"] = point_module
    sys.modules["models"] = types.ModuleType("models")
    sys.modules["models.architectural"] = types.ModuleType("models.architectural")
    sys.modules["models.architectural.wall_node"] = node_module

    source=Path(__file__).parents[1]/"src/engines/architectural/wall_network.py"
    spec=importlib.util.spec_from_file_location("wall_network_tested",source)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    WallNetwork=module.WallNetwork
finally:
    for name, previous in _previous_modules.items():
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous


class Wall:
    def __init__(self,*coords):
        self.path=[Point(*value) for value in coords]
        self.wall_node_ids=[]; self.wall_connections=[]; self.wall_network_revision=0
    def rebuild_wall_geometry(self): pass
    def _update_properties(self): pass


def node_at(network,x,y):
    return min(network.nodes,key=lambda node:(node.position.x-x)**2+(node.position.y-y)**2)


def test_l_join():
    first=Wall((0,0,0),(5,0,0)); second=Wall((5,0,0),(5,5,0))
    network=WallNetwork().rebuild([first,second])
    assert node_at(network,5,0).node_type=="L"


def test_t_join():
    horizontal=Wall((0,0,0),(10,0,0)); vertical=Wall((5,-5,0),(5,0,0))
    network=WallNetwork().rebuild([horizontal,vertical])
    assert node_at(network,5,0).node_type=="T"


def test_x_join():
    first=Wall((0,0,0),(10,10,0)); second=Wall((0,10,0),(10,0,0))
    network=WallNetwork().rebuild([first,second])
    assert node_at(network,5,5).node_type=="X"


def test_wall_metadata():
    first=Wall((0,0,0),(5,0,0)); second=Wall((5,0,0),(5,5,0))
    network=WallNetwork().rebuild([first,second])
    assert first.wall_network_revision==1
    assert first.wall_node_ids
    assert any(item["node_type"]=="L" for item in first.wall_connections)


if __name__ == "__main__":
    test_l_join(); test_t_join(); test_x_join(); test_wall_metadata()
    print("WALL NETWORK 5.0.4.3: L/T/X + metadata OK")
