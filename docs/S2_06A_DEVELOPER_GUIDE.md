# Developer Guide — Workspace

```python
from gui.workspace import DockArea, PanelDescriptor, WorkspaceManager

workspace = WorkspaceManager(".aias/layouts")
workspace.register_panel(
    PanelDescriptor("project_browser", "Navegador de proyecto", DockArea.LEFT)
)
workspace.panels.activate("project_browser")
workspace.open_document("projects/modelo.aias")
workspace.save_layout("Architecture")
```

Los paneles deben poseer identificadores estables. La GUI no debe modificar
`WorkspaceState` directamente: debe usar `WorkspaceManager`, `PanelManager` o
`DockManager`.
