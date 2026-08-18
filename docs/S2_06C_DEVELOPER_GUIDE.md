# Developer Guide — Project Browser

```python
from gui.project_browser import (
    ProjectBrowserBuilder,
    ProjectBrowserController,
    ProjectBrowserWidget,
)
from gui.workspace import DockArea, PanelDescriptor

model = ProjectBrowserBuilder().build(bim_objects)
controller = ProjectBrowserController(model, workspace=workspace)
widget = ProjectBrowserWidget(controller)

docking.register_panel(
    PanelDescriptor(
        "project_browser",
        "Navegador de proyecto",
        DockArea.LEFT,
    ),
    widget,
)
```
