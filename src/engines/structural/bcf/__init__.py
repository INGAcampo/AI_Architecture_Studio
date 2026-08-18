from dataclasses import dataclass, field
from enum import Enum
import json

class IssueStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass(frozen=True, slots=True)
class BcfIssue:
    issue_id: str
    title: str
    status: IssueStatus
    assigned_to: str | None = None
    related_element_ids: tuple[str, ...] = ()
    comments: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.issue_id.strip() or not self.title.strip():
            raise ValueError("Datos obligatorios")

class BcfIssueEngine:
    def __init__(self):
        self._issues = {}

    def add(self, issue):
        if issue.issue_id in self._issues:
            raise KeyError(issue.issue_id)
        self._issues[issue.issue_id] = issue
        return issue

    def export_json(self):
        return json.dumps({
            "issues": [{
                "issue_id": issue.issue_id,
                "title": issue.title,
                "status": issue.status.value,
                "assigned_to": issue.assigned_to,
                "related_element_ids": list(issue.related_element_ids),
                "comments": list(issue.comments),
            } for issue in self._issues.values()]
        }, sort_keys=True)

    def open_issues(self):
        return tuple(
            issue for issue in self._issues.values()
            if issue.status not in (IssueStatus.RESOLVED, IssueStatus.CLOSED)
        )
