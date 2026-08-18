# Developer Guide — Intelligent Roof System

```python
engine.register_type(roof_type)
engine.add_roof(
    IntelligentRoof(
        "roof-1",
        roof_type.type_id,
        boundary,
        pitch_degrees=30.0,
        overhang=0.60,
        ridge_length=10.0,
    )
)
quantities = engine.calculate_quantities("roof-1")
```
