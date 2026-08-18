# Developer Guide — Visual Docking

```python
from PySide6.QtWidgets import QLabel
from gui.workspace import (
    DockArea,
    PanelDescriptor,
    QtDockingController,
    WorkspaceManager,
)

workspace = WorkspaceManager(".aias/layouts")
docking = QtDockingController(main_window, workspace)

docking.register_panel(
    PanelDescriptor(
        "project_browser",
        "Navegador de proyecto",
        DockArea.LEFT,
    ),
    lambda: QLabel("Project Browser"),
)
```

Use identificadores estables para que `QMainWindow.saveState()` pueda restaurar
correctamente los paneles.
