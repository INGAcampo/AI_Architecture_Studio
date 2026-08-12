# Developer Guide — Formula Engine

```python
formula_engine.add_formula(
    FormulaDefinition(
        "wall.area",
        "wall-1",
        "area",
        "length * height",
    )
)
formula_engine.add_formula(
    FormulaDefinition(
        "wall.volume",
        "wall-1",
        "volume",
        "area * thickness",
    )
)
formula_engine.evaluate_owner("wall-1")
```
