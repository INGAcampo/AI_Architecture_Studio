from dataclasses import dataclass
from enum import Enum

class PublicationFormat(str, Enum):
    PDF = "pdf"
    DWG = "dwg"
    DXF = "dxf"

@dataclass(frozen=True, slots=True)
class PublicationRequest:
    sheet_ids: tuple[str, ...]
    output_format: PublicationFormat
    output_name: str

@dataclass(frozen=True, slots=True)
class PublicationResult:
    success: bool
    output_format: PublicationFormat
    output_name: str
    published_sheet_ids: tuple[str, ...]
    errors: tuple[str, ...] = ()

class Publisher:
    def publish(self, request, sheet_manager):
        errors = []
        published = []
        for sheet_id in request.sheet_ids:
            try:
                sheet_manager.get(sheet_id)
            except KeyError:
                errors.append(f"Hoja inexistente: {sheet_id}")
            else:
                published.append(sheet_id)
        return PublicationResult(
            success=not errors,
            output_format=request.output_format,
            output_name=request.output_name,
            published_sheet_ids=tuple(published),
            errors=tuple(errors),
        )
