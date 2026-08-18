from dataclasses import dataclass
import json

@dataclass(frozen=True, slots=True)
class ReportSection:
    title: str
    content: str
    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("title obligatorio")

class StructuralReportGenerator:
    def markdown(self, title, sections):
        lines = [f"# {title}", ""]
        for section in sections:
            lines.extend([f"## {section.title}", "", section.content, ""])
        return "\n".join(lines)
    def json_report(self, title, sections):
        return json.dumps({
            "title": title,
            "sections": [{"title": s.title, "content": s.content} for s in sections],
        }, sort_keys=True)
