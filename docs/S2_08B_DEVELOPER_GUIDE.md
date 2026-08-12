# Developer Guide — Parametric Engine

```python
from engines.parametric.parameters import (
    ParameterEngine,
    ParameterService,
    wall_parameter_schema,
)

engine = ParameterEngine()
service = ParameterService(engine)
wall = service.create_owner("wall-1", wall_parameter_schema())
service.edit("wall-1", "height", 4.20)
engine.set_calculated("wall-1", "area", 21.0)
```
