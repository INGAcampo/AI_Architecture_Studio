"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations

class IncrementalExecutionEngine:
    """Execute the public IncrementalExecutionEngine operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def changed_stages(self, previous: dict | None, current: dict) -> tuple[str, ...]:
        """Execute the public IncrementalExecutionEngine.changed_stages operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        if previous is None:
            return ("compile","generate_code","generate_tests","generate_docs","validate","certify","package")
        changed = []
        if previous.get("requirements") != current.get("requirements"):
            changed += ["compile","generate_code","generate_tests","generate_docs","validate","certify","package"]
        elif previous.get("documentation") != current.get("documentation"):
            changed += ["generate_docs","validate","certify","package"]
        elif previous.get("version") != current.get("version"):
            changed += ["validate","certify","package"]
        return tuple(dict.fromkeys(changed))
