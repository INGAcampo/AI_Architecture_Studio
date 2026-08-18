"""Boundary conversion between structural analysis and BIM member payloads."""
from .model import StructuralModel2D, Node2D, Material, Section, FrameElement2D

class BimStructuralAdapter:
    """Map model geometry and analysis results into traceable BIM properties."""
    def from_omega_project(self, project):
        """Execute the public BimStructuralAdapter.from_omega_project operation for the Omega structural analysis and design suite using explicit caller inputs."""
        model = StructuralModel2D()
        model.materials["DEFAULT"] = Material("DEFAULT", 200e9, 345e6, 7850)
        model.sections["DEFAULT"] = Section("DEFAULT", 0.01, 8.0e-5, 0.3)
        for obj in project.objects.values():
            if obj.object_type == "structural_node":
                model.nodes[str(obj.object_id)] = Node2D(
                    str(obj.object_id),
                    float(obj.geometry["x"]),
                    float(obj.geometry["y"]),
                    bool(obj.properties.get("fix_x", False)),
                    bool(obj.properties.get("fix_y", False)),
                    bool(obj.properties.get("fix_rz", False)),
                )
        for obj in project.objects.values():
            if obj.object_type == "structural_member":
                model.elements[str(obj.object_id)] = FrameElement2D(
                    str(obj.object_id),
                    obj.properties["node_i"],
                    obj.properties["node_j"],
                    "DEFAULT",
                    "DEFAULT",
                )
        return model
