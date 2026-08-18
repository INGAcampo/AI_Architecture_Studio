"""Public module supporting the coordinated multi-studio desktop shell."""
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from .project_model import AiasProject, ProjectNode

class ProjectExplorer(QTreeWidget):
    """Execute the public ProjectExplorer operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self, project: AiasProject, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderLabels(["Proyecto"])
        self.refresh(project)

    def refresh(self, project: AiasProject) -> None:
        """Execute the public ProjectExplorer.refresh operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        self.clear()
        root = QTreeWidgetItem([project.name])
        self.addTopLevelItem(root)
        for child in project.root_node.children:
            root.addChild(self._item(child))
        root.setExpanded(True)

    def _item(self, node: ProjectNode) -> QTreeWidgetItem:
        item = QTreeWidgetItem([node.name])
        for child in node.children:
            item.addChild(self._item(child))
        return item
