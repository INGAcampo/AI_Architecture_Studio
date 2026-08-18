"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations

class IntelligentTemplateSelector:
    """Execute the public IntelligentTemplateSelector operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def select(self, specification: dict, available: list[dict]) -> dict:
        """Execute the public IntelligentTemplateSelector.select operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        domain = specification.get("domain", "generic")
        capability = specification.get("capability", "")
        scored = []
        for template in available:
            score = 0
            if template.get("domain") == domain:
                score += 10
            if capability and capability in template.get("capabilities", []):
                score += 5
            score += int(template.get("priority", 0))
            scored.append((score, template))
        if not scored:
            raise ValueError("No templates available.")
        scored.sort(key=lambda item: (-item[0], item[1].get("template_id", "")))
        return scored[0][1]
