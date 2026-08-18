# Developer Guide — Intelligent Openings

```python
engine.register_wall(
    HostWallGeometry("wall-1", 8.0, 3.0, 0.20)
)
engine.add_opening(
    Opening(
        "door-1",
        "wall-1",
        OpeningKind.DOOR,
        0.90,
        2.10,
        OpeningPlacement(offset=1.0),
    )
)
```
