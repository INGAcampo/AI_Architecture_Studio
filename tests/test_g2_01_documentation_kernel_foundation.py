import pytest

from documentation_kernel import (
    Annotation,
    AnnotationKind,
    DocumentationKernel,
    DocumentationView,
    GraphicStyle,
    PublicationRequest,
    Publisher,
    Sheet,
    Viewport,
)
from documentation_kernel.publisher import PublicationFormat


@pytest.mark.parametrize("index", range(20))
def test_views_and_annotations(index):
    kernel = DocumentationKernel()
    kernel.styles.register(GraphicStyle("default"))
    kernel.views.add(DocumentationView(f"V{index}", "Planta", 100))
    updated = kernel.views.add_annotation(
        f"V{index}",
        Annotation(f"A{index}", AnnotationKind.TEXT, "Nota", 10, 20),
    )
    assert len(updated.annotations) == 1
    assert updated.annotations[0].text == "Nota"


@pytest.mark.parametrize("index", range(20))
def test_sheets_and_viewports(index):
    kernel = DocumentationKernel()
    kernel.sheets.add(Sheet(f"S{index}", f"A-{index}", "Plano", 841, 594))
    sheet = kernel.sheets.place_viewport(
        f"S{index}",
        Viewport(f"VP{index}", "V1", 10, 10, 200, 150),
    )
    assert len(sheet.viewports) == 1
    with pytest.raises(ValueError):
        kernel.sheets.place_viewport(
            f"S{index}",
            Viewport(f"VPX{index}", "V2", 50, 50, 200, 150),
        )


@pytest.mark.parametrize("index", range(20))
def test_styles(index):
    kernel = DocumentationKernel()
    kernel.styles.register(
        GraphicStyle(f"style-{index}", text_height=3.0, line_weight=0.35)
    )
    style = kernel.styles.get(f"style-{index}")
    assert style.text_height == 3.0
    assert style.line_weight == 0.35


@pytest.mark.parametrize("index", range(20))
def test_synchronization(index):
    kernel = DocumentationKernel()
    kernel.views.add(DocumentationView(f"V{index}", "Corte", 50, model_revision=1))
    report = kernel.synchronize(3)
    assert report.updated_view_ids == (f"V{index}",)
    assert kernel.views.get(f"V{index}").model_revision == 3


@pytest.mark.parametrize("index", range(20))
def test_validation(index):
    kernel = DocumentationKernel()
    kernel.views.add(
        DocumentationView(
            f"V{index}",
            "Alzado",
            100,
            annotations=(
                Annotation(
                    f"A{index}",
                    AnnotationKind.TAG,
                    "P-01",
                    0,
                    0,
                    style_id="missing",
                ),
            ),
        )
    )
    kernel.sheets.add(Sheet(f"S{index}", f"A-{index}", "Hoja vacía", 841, 594))
    issues = kernel.validate()
    assert {issue.code for issue in issues} == {"missing_style", "empty_sheet"}


@pytest.mark.parametrize("index", range(20))
def test_publication(index):
    kernel = DocumentationKernel()
    kernel.sheets.add(Sheet(f"S{index}", f"A-{index}", "Plano", 841, 594))
    result = kernel.publisher.publish(
        PublicationRequest(
            sheet_ids=(f"S{index}",),
            output_format=PublicationFormat.PDF,
            output_name=f"set-{index}.pdf",
        ),
        kernel.sheets,
    )
    assert result.success
    assert result.published_sheet_ids == (f"S{index}",)
