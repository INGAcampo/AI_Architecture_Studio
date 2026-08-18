from engines.architectural.wall_engine import WallEngine
from engines.architectural.wall_network import WallNetwork
from engines.architectural.wall_node_editor import WallNodeEditor
from engines.geometry.point import Point


class Scene:
    def __init__(self, elements):
        self.elements = elements
    def get_elements(self):
        return self.elements


def test_move_t_node():
    horizontal = WallEngine.create_wall([Point(0,0,0), Point(10,0,0)])
    vertical = WallEngine.create_wall([Point(5,-5,0), Point(5,0,0)])
    scene = Scene([horizontal, vertical])
    network = WallNetwork.ensure_scene(scene)
    t_nodes = [n for n in network.nodes if n.node_type == "T"]
    assert len(t_nodes) == 1
    before, after = WallNodeEditor.move_node(scene, t_nodes[0], Point(6,1,0))
    assert before and after
    assert any(abs(p.x-6)<1e-9 and abs(p.y-1)<1e-9 for p in vertical.path)
    assert any(abs(p.x-6)<1e-9 and abs(p.y-1)<1e-9 for p in horizontal.path)
