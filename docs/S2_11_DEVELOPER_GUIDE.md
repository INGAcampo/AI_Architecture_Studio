# Developer Guide — Intelligent Slabs

```python
slab_type = SlabType(
    "floor-250",
    "Floor 250 mm",
    SlabStructure(
        (
            SlabLayer("finish", "Finish", SlabLayerFunction.FINISH, 0.03),
            SlabLayer("core", "Core", SlabLayerFunction.STRUCTURE, 0.20),
            SlabLayer("ceiling", "Ceiling", SlabLayerFunction.FINISH, 0.02),
        )
    ),
)
engine.register_type(slab_type)
engine.add_slab(
    IntelligentSlab(
        "slab-1",
        "floor-250",
        (
            Point2D(0, 0),
            Point2D(8, 0),
            Point2D(8, 6),
            Point2D(0, 6),
        ),
    )
)
```
