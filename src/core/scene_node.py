"""
AI Architecture Studio
Scene Node

Foundation 1.5
"""


class SceneNode:
    def __init__(self, name, node_type="Folder"):
        self.name = name
        self.node_type = node_type
        self.children = []
        self.parent = None
        self.element = None

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def remove_child(self, node):
        if node in self.children:
            self.children.remove(node)
            node.parent = None

    def __repr__(self):
        return f"<{self.node_type}: {self.name}>"