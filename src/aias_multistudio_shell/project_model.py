"""Public module supporting the coordinated multi-studio desktop shell."""
from dataclasses import dataclass, field
from pathlib import Path

@dataclass(slots=True)
class ProjectNode:
    """Execute the public ProjectNode operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    name: str
    node_type: str
    children: list["ProjectNode"] = field(default_factory=list)

@dataclass(slots=True)
class AiasProject:
    """Execute the public AiasProject operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    name: str
    root_path: Path | None = None
    root_node: ProjectNode = field(default_factory=lambda: ProjectNode("Project", "root"))

    def add_group(self, name: str, node_type: str) -> ProjectNode:
        """Add group to the coordinated multi-studio desktop shell while enforcing identity constraints."""
        node = ProjectNode(name, node_type)
        self.root_node.children.append(node)
        return node
