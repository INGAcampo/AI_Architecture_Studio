from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True, slots=True)
class Revision:
    revision_id: str
    description: str
    issued_on: date
    author: str

@dataclass(frozen=True, slots=True)
class TitleBlock:
    titleblock_id: str
    project_name: str
    sheet_number: str
    sheet_title: str
    revisions: tuple[Revision, ...] = ()

class TitleBlockRevisionManager:
    def add_revision(self, titleblock, revision):
        return TitleBlock(
            titleblock.titleblock_id,
            titleblock.project_name,
            titleblock.sheet_number,
            titleblock.sheet_title,
            titleblock.revisions + (revision,),
        )

    def latest_revision(self, titleblock):
        return max(titleblock.revisions, key=lambda revision: revision.issued_on) if titleblock.revisions else None
