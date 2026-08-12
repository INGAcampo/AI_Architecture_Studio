"""Unique coordination-issue registration and controlled resolution."""
from __future__ import annotations

from .models import CoordinationIssue, IssueStatus


class IssueRegister:
    """Prevent duplicate issues, resolve owned findings and report open workload."""
    def __init__(self, issues: list[CoordinationIssue] | None = None):
        self.issues = list(issues or [])

    def add(self, issue: CoordinationIssue) -> None:
        """Add a uniquely identified coordination issue."""
        if any(current.issue_id == issue.issue_id for current in self.issues):
            raise ValueError(f"duplicate_issue:{issue.issue_id}")
        self.issues.append(issue)

    def resolve(self, issue_id: str, resolution: str) -> None:
        """Resolve an existing issue with explicit resolution evidence."""
        for issue in self.issues:
            if issue.issue_id == issue_id:
                issue.status = IssueStatus.RESOLVED
                issue.resolution = resolution
                return
        raise KeyError(issue_id)

    @property
    def open_count(self) -> int:
        """Return the number of issues that remain open."""
        return sum(issue.status == IssueStatus.OPEN for issue in self.issues)
