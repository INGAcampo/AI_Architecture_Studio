# Developer Guide — Intelligent Wall System

```python
wall_type = WallType(
    "basic-200",
    "Basic Wall 200 mm",
    CompoundStructure(
        (
            WallLayer("finish-ext", "Exterior", WallLayerFunction.FINISH, 0.02),
            WallLayer("core", "Core", WallLayerFunction.STRUCTURE, 0.16),
            WallLayer("finish-int", "Interior", WallLayerFunction.FINISH, 0.02),
        )
    ),
)
engine.register_type(wall_type)
engine.add_wall(IntelligentWall("wall-1", "basic-200", 8.0, 0.0, 3.0))
```
