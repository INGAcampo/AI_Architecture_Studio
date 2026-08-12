from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class QAIssue:
    code: str
    severity: str
    object_id: str
    message: str

class DocumentationQAAutomation:
    def review(self, sheets, views):
        issues = []
        view_ids = {view["view_id"] for view in views}
        sheet_numbers = set()
        for sheet in sheets:
            number = sheet["number"]
            if number in sheet_numbers:
                issues.append(QAIssue("duplicate_sheet_number", "error", sheet["sheet_id"], number))
            sheet_numbers.add(number)
            if not sheet.get("view_ids"):
                issues.append(QAIssue("empty_sheet", "warning", sheet["sheet_id"], "Hoja vacía"))
            for view_id in sheet.get("view_ids", ()):
                if view_id not in view_ids:
                    issues.append(QAIssue("missing_view", "error", sheet["sheet_id"], view_id))
        return tuple(issues)

    def summary(self, issues):
        return {
            "total": len(issues),
            "errors": sum(issue.severity == "error" for issue in issues),
            "warnings": sum(issue.severity == "warning" for issue in issues),
        }
