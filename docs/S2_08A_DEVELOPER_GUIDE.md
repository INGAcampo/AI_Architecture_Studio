# Developer Guide — Constraint Engine

```python
from engines.parametric.constraints import *

service = ConstraintService()
service.geometry.set_element(
    "wall-1",
    "axis",
    ConstraintSegment(
        ConstraintPoint(0, 0),
        ConstraintPoint(5, 0),
    ),
)
service.add_constraint(
    ConstraintDefinition(
        "wall-1-horizontal",
        ConstraintKind.HORIZONTAL,
        (ConstraintTarget("wall-1", "axis"),),
    )
)
report = service.solve()
assert report.success
```
