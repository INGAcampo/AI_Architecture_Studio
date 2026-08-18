"""Explicit project-brief contract for technical-file generation."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ProjectBrief:
    """Declare project identity, scope, location, discipline and review boundary."""
    project_id:str;title:str;location:str;client:str;scope:str;discipline:str;revision:str="R00";prepared_by:str="AIAS";checked_by:str="PROFESSIONAL_REVIEW_REQUIRED"
    def validate(self):
        """Reject incomplete project identity or uncontrolled revision labels."""
        if not all((self.project_id,self.title,self.location,self.client,self.scope,self.discipline,self.prepared_by,self.checked_by)):raise ValueError("incomplete_project_brief")
        if not self.revision.startswith("R") or not self.revision[1:].isdigit():raise ValueError("invalid_revision")
