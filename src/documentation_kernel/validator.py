from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DocumentationIssue:
    code: str
    message: str
    object_id: str

class DocumentationValidator:
    def validate(self, view_manager, sheet_manager, style_registry):
        issues = []
        style_ids = {style.style_id for style in style_registry.all()}
        view_ids = {view.view_id for view in view_manager.all()}

        for view in view_manager.all():
            for annotation in view.annotations:
                if annotation.style_id not in style_ids:
                    issues.append(
                        DocumentationIssue(
                            "missing_style",
                            f"Estilo inexistente: {annotation.style_id}",
                            annotation.annotation_id,
                        )
                    )

        for sheet in sheet_manager.all():
            if not sheet.viewports:
                issues.append(
                    DocumentationIssue(
                        "empty_sheet",
                        "La hoja no contiene viewports",
                        sheet.sheet_id,
                    )
                )
            for viewport in sheet.viewports:
                if viewport.view_id not in view_ids:
                    issues.append(
                        DocumentationIssue(
                            "missing_view",
                            f"Vista inexistente: {viewport.view_id}",
                            viewport.viewport_id,
                        )
                    )
        return tuple(issues)
