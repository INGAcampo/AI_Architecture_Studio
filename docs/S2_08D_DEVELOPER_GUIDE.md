# Developer Guide — Regeneration Engine

```python
engine.register(
    RegenerationItem(
        "wall-1",
        regenerate_wall,
        priority=10,
    )
)
engine.register(
    RegenerationItem(
        "door-1",
        regenerate_door,
        dependencies=("wall-1",),
    )
)
engine.regenerate()
```
