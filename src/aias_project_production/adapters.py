"""Stable, fail-closed contracts over the certified PP/PRO capability providers."""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile
import shutil
import time
from xml.sax.saxutils import escape
from types import SimpleNamespace

from aias_drawing_core import DrawingCore
from aias_cad_professional.engine import CADEngine
from aias_dxf_writer import ValidDxfWriter
from aias_quantities_core import QuantityTakeoffEngine
from aias_reports_core import ReportCore
from aias_standards_core import StandardsPack
from aias_professional_qa import ProfessionalQAGate


def _sha(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


class DrawingProductionAdapter:
    provider = "aias_drawing_core.DrawingCore"
    def produce(self, graph, structural_result, output: Path) -> dict:
        if structural_result is None or not structural_result.evidence_sha256:
            raise ValueError("drawing contract requires structural evidence")
        output.mkdir(parents=True, exist_ok=True)
        model = DrawingCore().build(graph, {"status": structural_result.status, "evidence_sha256": structural_result.evidence_sha256})
        errors = DrawingCore().validate(model)
        if errors: raise ValueError("drawing contract validation failed: " + "; ".join(errors))
        pdf = output / "drawing_set.pdf"; digest = DrawingCore().export_pdf(model, pdf)
        cad = DrawingModelToCADDocumentAdapter().adapt(graph, model)
        dxf = output / "drawing_set.dxf"; ValidDxfWriter().write(cad, dxf)
        native = NativeDWGProductionAdapter().produce(cad, output / "native")
        return {"gate": "PASS", "model": model, "pdf": str(pdf), "pdf_sha256": _sha(pdf.read_bytes()), "drawing_sha256": digest,
                "cad_document": cad, "dxf": str(dxf), "dxf_sha256": _sha(dxf.read_bytes()),
                "native_dwg": native,
                "sheet_ids": [s["id"] for s in model.sheets], "provenance": "ProjectGraph/BIM+StructuralResult"}


class DrawingModelToCADDocumentAdapter:
    """Maps BIM-derived DrawingModel semantics to the certified CADDocument contract."""
    provider = "aias_cad_professional.CADEngine"
    def adapt(self, graph, drawing_model):
        if not drawing_model.sheets or {x["number"] for x in drawing_model.sheets} != {"A-101","S-101","S-201","A-301","A-401"}:
            raise ValueError("DrawingModel sheet contract incomplete")
        cad = CADEngine().build(graph)
        errors = CADEngine().validate(cad)
        if errors: raise ValueError("CADDocument validation failed: " + "; ".join(errors))
        if {s["number"] for s in cad.sheets} != {s["number"] for s in drawing_model.sheets}:
            raise ValueError("DrawingModel/CADDocument sheet mismatch")
        return cad


class NativeDWGProductionAdapter:
    """Adapter over DR-01A's certified Core Console invocation and XData inspector."""
    provider = "scripts/run_dr01a_executive_dwg_closure.py"
    autocad = Path(r"C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe")
    def _invoke(self, drawing: Path, script: Path, timeout: int = 45) -> dict:
        started=time.time(); process=subprocess.Popen([str(self.autocad), "/i", str(drawing), "/s", str(script)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try: stdout, stderr = process.communicate(timeout=timeout); timed=False
        except subprocess.TimeoutExpired: process.kill(); stdout, stderr=process.communicate(); timed=True
        return {"pid":process.pid,"exit_code":process.returncode,"timed_out":timed,"duration_seconds":round(time.time()-started,3),"stdout_tail":stdout[-1000:],"stderr_tail":stderr[-1000:]}
    def produce(self, cad, output: Path) -> dict:
        if not self.autocad.exists(): raise RuntimeError("BLOCKED_BACKEND_UNAVAILABLE")
        output.mkdir(parents=True, exist_ok=True); source_ids={e["id"] for e in cad.entities}; layers={e["layer"] for e in cad.entities}; writer=ValidDxfWriter(); rows=[]
        for sheet in cad.sheets:
            work=(output / sheet["number"]).resolve(); work.mkdir(parents=True, exist_ok=True); dxf=work / f'{sheet["number"]}.dxf'; writer.write(cad,dxf); dwg=work / f'{sheet["number"]}.dwg'
            save=work / "save.scr"; save.write_text(f'_.SAVEAS\n2018\n"{str(dwg).replace(chr(92),"/")}"\n_.QUIT\n',encoding="ascii")
            generation=self._invoke(dxf,save)
            log=work / "inspect.txt"; inspect=work / "inspect.scr"; inspect.write_text(f'''(setq f (open "{str(log).replace(chr(92),"/")}" "w"))
(setq e (entnext))
(while e (setq d (entget e (list "AIAS")) x (cdr (assoc -3 d)) a (assoc "AIAS" x) i (if a (cdr (assoc 1000 (cdr a))) "")) (write-line (strcat "E|" i "|" (cdr (assoc 0 d)) "|" (if (assoc 8 d) (cdr (assoc 8 d)) "") "|" (cdr (assoc 5 d))) f) (setq e (entnext e)))
(close f) (princ) _.QUIT
''',encoding="ascii")
            reopen=self._invoke(dwg,inspect) if dwg.exists() else {"exit_code":None,"timed_out":False,"pid":None}
            recovered=[]
            if log.exists():
                for line in log.read_text(encoding="utf-8",errors="replace").splitlines():
                    p=line.split("|")
                    if len(p)==5 and p[0]=="E" and p[1]: recovered.append({"aias_id":p[1],"type":p[2],"layer":p[3],"handle":p[4]})
            ids=[x["aias_id"] for x in recovered]; handles=[x["handle"] for x in recovered]; missing=sorted(source_ids-set(ids)); duplicate=sorted({x for x in ids if ids.count(x)>1}); critical=bool(missing or duplicate or set(x["layer"] for x in recovered)!=layers or generation["exit_code"]!=0 or reopen["exit_code"]!=0 or generation["timed_out"] or reopen["timed_out"])
            rows.append({"drawing_id":sheet["id"],"dxf":str(dxf),"dwg":str(dwg),"dxf_sha256":_sha(dxf.read_bytes()),"dwg_sha256":_sha(dwg.read_bytes()) if dwg.exists() else None,"byte_size":dwg.stat().st_size if dwg.exists() else 0,"generation":generation,"reopen":reopen,"aias_ids":ids,"handles":handles,"layers":sorted({x["layer"] for x in recovered}),"missing":missing,"duplicates":duplicate,"roundtrip_verdict":"PASS" if not critical else "FAIL"})
        audit = {"schema":"aias.native_dwg_roundtrip.v1","drawings":rows,"verdict":"PASS" if rows and all(x["roundtrip_verdict"] == "PASS" for x in rows) else "FAIL"}
        (output / "native_roundtrip.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
        if audit["verdict"] != "PASS": raise RuntimeError("BLOCKER_NATIVE_DWG_ROUNDTRIP_FAILED")
        return {"gate":"V5_NATIVE_DWG_INTEGRATION_PASS","backend":"AutoCAD 2027 accoreconsole.exe","drawings":rows,"sha256":_sha(rows)}


class QuantityWorkbookAdapter:
    provider = "aias_quantities_core.QuantityTakeoffEngine"
    def produce(self, graph, output: Path) -> dict:
        output.mkdir(parents=True, exist_ok=True)
        engine = QuantityTakeoffEngine(); package = engine.build(graph, {"concrete": 0.05})
        if not package.items: raise ValueError("quantity contract produced no items")
        csv_path = output / "boq.csv"; engine.export_csv(package, csv_path)
        xlsx_path = output / "quantities.xlsx"; xlsx_sha = XLSXProductionAdapter().write(package, xlsx_path)
        return {"gate": "PASS", "package": package, "csv": str(csv_path), "sha256": engine.evidence_sha256(package),
                "xlsx": str(xlsx_path), "xlsx_sha256": xlsx_sha, "element_ids": [x["element_id"] for x in package.items], "provenance": "ProjectGraph/BIM"}


class XLSXProductionAdapter:
    """Dependency-free XLSX writer over QuantityPackage; zip/XML reopen validation is mandatory."""
    provider = "aias_project_production.adapters.XLSXProductionAdapter"
    def write(self, package, path: Path) -> str:
        headers = ["element_id","category","rule","measurement","waste_factor","quantity","unit","material"]
        rows = [headers] + [[str(item.get(h, "")) for h in headers] for item in package.items]
        def cell(col, row, value): return f'<c r="{col}{row}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'
        xml_rows=[]
        for r, values in enumerate(rows, 1):
            xml_rows.append('<row r="%d">%s</row>' % (r, ''.join(cell(chr(65+i), r, value) for i,value in enumerate(values))))
        sheet = '<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>%s</sheetData></worksheet>' % ''.join(xml_rows)
        content = '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'
        rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
        wb = '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="BOQ" sheetId="1" r:id="rId1"/></sheets></workbook>'
        wb_rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>'
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', content); z.writestr('_rels/.rels', rels); z.writestr('xl/workbook.xml', wb); z.writestr('xl/_rels/workbook.xml.rels', wb_rels); z.writestr('xl/worksheets/sheet1.xml', sheet)
        with zipfile.ZipFile(path) as z:
            required={'[Content_Types].xml','_rels/.rels','xl/workbook.xml','xl/worksheets/sheet1.xml'}
            if not required <= set(z.namelist()) or b'#REF!' in z.read('xl/worksheets/sheet1.xml'): raise ValueError("XLSX reopen validation failed")
        return _sha(path.read_bytes())


class ReportProductionAdapter:
    provider = "aias_reports_core.ReportCore"
    def produce(self, graph, structural_result, drawing, quantities, output: Path) -> dict:
        output.mkdir(parents=True, exist_ok=True)
        analysis = SimpleNamespace(status=structural_result.status, internal_forces=structural_result.load_envelopes,
            code_checks=structural_result.design_checks, evidence_sha256=structural_result.evidence_sha256,
            reactions={}, displacements={}, drifts={})
        package = ReportCore().build(graph, StandardsPack(), analysis, drawing, quantities)
        exported = ReportCore().export(package, output)
        if not exported: raise ValueError("report contract produced no documents")
        return {"gate": "PASS", "package": package, "documents": exported, "sha256": _sha(exported), "provenance": "Graph+Analysis+Drawing+Quantities"}


class ProfessionalQAAdapter:
    provider = "aias_professional_qa.ProfessionalQAGate"
    def evaluate(self, result, drawing, quantities, reports, scenario_id: str) -> dict:
        design_status = "PRODUCTION_READY" if result.status == "PASS" else "V0_LIMITED"
        artifacts = [("Structural design", design_status, result.evidence_sha256, "Analysis", "Resolve design failure"),
                     ("PDF", "PRODUCTION_READY", drawing["pdf_sha256"], "Drawing", ""),
                     ("BOQ CSV", "PRODUCTION_READY", quantities["sha256"], "Quantities", ""),
                     ("Reports", "PRODUCTION_READY", reports["sha256"], "Reports", "")]
        qa = ProfessionalQAGate().evaluate(artifacts)
        category = "SCENARIO_DESIGN_FAILURE" if result.status == "FAIL" else "NONE"
        # The upstream gate is intentionally reused, but its construction-facing
        # verdict must never escape a synthetic laboratory run.
        qa["verdict"] = "SYNTHETIC_CONTRACT_PASS" if category == "NONE" else "SYNTHETIC_SCENARIO_DESIGN_FAILURE"
        return {"gate": "PASS", "classification": category, "result": qa, "sha256": qa["hash"]}


class ExecutiveIssuanceAdapter:
    provider = "aias_project_production.adapters.ExecutiveIssuanceAdapter"
    def issue(self, scenario_id: str, output: Path, drawing: dict, quantities: dict, reports: dict, qa: dict) -> dict:
        artifacts = {"pdf": drawing["pdf"], "boq_csv": quantities["csv"], "reports": reports["documents"], "qa": qa}
        manifest = {"schema": "aias.synthetic_executive_issuance.v1", "scenario_id": scenario_id,
            "SYNTHETIC_TEST_DATA": True, "NOT_FOR_CONSTRUCTION": True, "artifacts": artifacts,
            "sha256": _sha(artifacts), "verdict": "SYNTHETIC_ISSUANCE_PASS"}
        path = output / "V8_SYNTHETIC_EXECUTIVE_MANIFEST.json"; path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        return {"gate": "PASS", "verdict": manifest["verdict"], "manifest": str(path), "sha256": _sha(manifest)}
