# Developer Guide — Intelligent Structural Frame

```python
engine.register_material(material)
engine.register_profile(profile)
engine.add_member(
    StructuralMember(
        "beam-1",
        StructuralElementKind.BEAM,
        StructuralPoint(0, 0, 3),
        StructuralPoint(6, 0, 3),
        profile.profile_id,
        material.material_id,
    )
)
```
