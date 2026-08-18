from storage.object_graph import ObjectGraphCodec


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Node:
    def __init__(self, name="root"):
        self.name = name
        self.children = []


def test_object_graph_roundtrip():
    root = Node()
    point = Point(3.5, 7.0)
    root.children = [point, point]
    decoded = ObjectGraphCodec().decode(ObjectGraphCodec().encode(root))
    assert decoded.name == "root"
    assert decoded.children[0].x == 3.5
    assert decoded.children[0] is decoded.children[1]
