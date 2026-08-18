from dataclasses import dataclass
from enum import Enum

class PublishFormat(str, Enum):
    PDF = "pdf"
    DWG = "dwg"
    DXF = "dxf"

@dataclass(frozen=True, slots=True)
class PublishJob:
    job_id: str
    sheet_ids: tuple[str, ...]
    output_format: PublishFormat
    destination: str

@dataclass(frozen=True, slots=True)
class PublishManifest:
    job_id: str
    files: tuple[str, ...]
    success: bool

class ProfessionalPublisher:
    def publish(self, job):
        extension = job.output_format.value
        files = tuple(
            f"{job.destination.rstrip('/')}/{sheet_id}.{extension}"
            for sheet_id in job.sheet_ids
        )
        return PublishManifest(job.job_id, files, True)
