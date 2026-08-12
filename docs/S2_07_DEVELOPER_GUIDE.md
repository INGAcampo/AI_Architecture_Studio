# Developer Guide — BIM Workspace Suite

```python
from gui.bim_workspace import (
    BimWorkspaceBuilder,
    BimWorkspaceController,
    BimWorkspaceWidget,
)

tree = BimWorkspaceBuilder().build(
    bim_objects,
    materials=material_catalog,
    families=family_catalog,
)
controller = BimWorkspaceController(tree, workspace=workspace)
widget = BimWorkspaceWidget(controller)
```
