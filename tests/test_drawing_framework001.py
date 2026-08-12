from pathlib import Path
import pytest
from aias_drawing_framework import DrawingExporter,DrawingValidator,Text
from aias_drawing_framework.reference import foundation_sheet
def test_reference_sheet_is_structurally_valid():assert DrawingValidator().validate(foundation_sheet())==[]
def test_all_vector_formats_and_checksums_are_created(tmp_path):
 result=DrawingExporter().export(foundation_sheet(),tmp_path);assert set(result["formats"])=={"json","svg","dxf","pdf"} and all(len(x["sha256"])==64 for x in result["formats"].values())
 assert (tmp_path/"DRW-FOUND-001.svg").read_text().startswith("<svg") and (tmp_path/"DRW-FOUND-001.pdf").read_bytes().startswith(b"%PDF-1.4")
def test_dxf_contains_portable_lines_and_text(tmp_path):
 DrawingExporter().export(foundation_sheet(),tmp_path);text=(tmp_path/"DRW-FOUND-001.dxf").read_text();assert "SECTION" in text and "LINE" in text and "TEXT" in text and text.rstrip().endswith("EOF")
def test_invalid_layer_and_unsafe_text_are_rejected(tmp_path):
 drawing=foundation_sheet();bad=type(drawing)(drawing.drawing_id,drawing.version,drawing.sheet,drawing.layers,drawing.views,drawing.entities+(Text("BAD","UNKNOWN",1,1,"<script>"),),drawing.provenance,True)
 issues=DrawingValidator().validate(bad);assert "unknown_layer:BAD" in issues and "unsafe_text:BAD" in issues
 with pytest.raises(ValueError,match="invalid_drawing"):DrawingExporter().export(bad,tmp_path)
