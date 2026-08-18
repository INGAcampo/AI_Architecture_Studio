"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from pathlib import Path
import re
from .models import DomainTemplate, GeneratedModule

def safe_identifier(value: str) -> str:
    """Execute the public safe_identifier operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_")
    if not value:
        value = "Generated"
    if value[0].isdigit():
        value = "Generated_" + value
    return value

class DomainTemplateEngine:
    """Execute the public DomainTemplateEngine operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def render(self, template: DomainTemplate, values: dict[str, str], output: Path) -> GeneratedModule:
        """Execute the public DomainTemplateEngine.render operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        output.mkdir(parents=True, exist_ok=True)
        module_name = values["module_name"]
        package = output / "src" / module_name
        package.mkdir(parents=True, exist_ok=True)

        artifacts = []
        for relative, content in template.files.items():
            rendered = content
            for key, value in values.items():
                rendered = rendered.replace("{{" + key + "}}", str(value))
            path = package / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8")
            artifacts.append(path)

        return GeneratedModule(
            module_name=module_name,
            root=output,
            artifacts=artifacts,
            metadata={"template_id": template.template_id, "domain": values.get("domain", "")},
        )
