# Developer Guide — Property Palette Pro

```python
from gui.property_palette import (
    PropertyPaletteController,
    PropertyPaletteModel,
    PropertyPaletteWidget,
    PropertySchemaRegistry,
    PropertySelectionAdapter,
    default_wall_schema,
)
from gui.workspace import DockArea, PanelDescriptor

schemas = PropertySchemaRegistry()
schemas.register("Wall", default_wall_schema())

controller = PropertyPaletteController(
    PropertyPaletteModel(),
    PropertySelectionAdapter(schemas),
    history_manager=history_manager,
    event_dispatcher=event_dispatcher,
)
widget = PropertyPaletteWidget(controller)

docking.register_panel(
    PanelDescriptor(
        "property_palette",
        "Propiedades",
        DockArea.RIGHT,
    ),
    widget,
)
```
