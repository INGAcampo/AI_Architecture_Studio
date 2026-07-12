"""
AI Architecture Studio
Scene Manager

Foundation 3.1
"""

from core.scene_node import SceneNode


class SceneManager:
    def __init__(self, kernel=None):
        self.kernel = kernel

        self.root = SceneNode("Proyecto AIAS", "Project")

        self.architecture = SceneNode("Arquitectura", "Discipline")
        self.structure = SceneNode("Estructuras", "Discipline")
        self.bim = SceneNode("BIM", "Discipline")
        self.documentation = SceneNode("Documentación", "Discipline")

        self.root.add_child(self.architecture)
        self.root.add_child(self.structure)
        self.root.add_child(self.bim)
        self.root.add_child(self.documentation)

        self.elements = []

    def add_element(self, element, discipline="Arquitectura"):
        self.elements.append(element)

        if self.kernel:
            registry = self.kernel.services.get("object_registry")
            event_bus = self.kernel.services.get("event_bus")

            if registry and hasattr(element, "id"):
                registry.register(element)

            if event_bus:
                event_bus.emit("scene.element_added", element)

        node = SceneNode(
            getattr(element, "name", "Elemento"),
            getattr(
                element,
                "element_type",
                getattr(element, "object_type", "Element"),
            ),
        )
        node.element = element

        if discipline == "Estructuras":
            self.structure.add_child(node)
        elif discipline == "BIM":
            self.bim.add_child(node)
        elif discipline == "Documentación":
            self.documentation.add_child(node)
        else:
            self.architecture.add_child(node)

    def remove_element(self, element):
        if element not in self.elements:
            return False

        self.elements.remove(element)
        self._remove_element_node(self.root, element)

        if self.kernel:
            registry = self.kernel.services.get("object_registry")
            event_bus = self.kernel.services.get("event_bus")

            if registry and hasattr(element, "id"):
                registry.unregister(element.id)

            if event_bus:
                event_bus.emit("scene.element_removed", element)

        return True

    def _remove_element_node(self, parent_node, element):
        for child in list(parent_node.children):
            if child.element is element:
                parent_node.remove_child(child)
                return True

            if self._remove_element_node(child, element):
                return True

        return False

    def get_elements(self):
        return self.elements.copy()

    def count(self):
        return len(self.elements)

    def summary(self):
        return [element.info() for element in self.elements]