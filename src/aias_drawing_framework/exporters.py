"""Deterministic JSON, SVG, ASCII DXF and minimal vector PDF exporters."""
from __future__ import annotations
import hashlib,html,json
from pathlib import Path
from .models import Dimension,Drawing,Line,Text
from .validation import DrawingValidator

class DrawingExporter:
    """Export a validated canonical drawing into auditable portable formats."""
    def export(self,drawing:Drawing,output:Path)->dict:
        """Write JSON, SVG, DXF and PDF files plus a checksum manifest."""
        issues=DrawingValidator().validate(drawing)
        if issues:raise ValueError("invalid_drawing:"+",".join(issues))
        output.mkdir(parents=True,exist_ok=True);files={"json":output/f"{drawing.drawing_id}.json","svg":output/f"{drawing.drawing_id}.svg","dxf":output/f"{drawing.drawing_id}.dxf","pdf":output/f"{drawing.drawing_id}.pdf"}
        files["json"].write_text(json.dumps(drawing.to_dict(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8");files["svg"].write_text(self._svg(drawing),encoding="utf-8");files["dxf"].write_text(self._dxf(drawing),encoding="ascii");files["pdf"].write_bytes(self._pdf(drawing))
        manifest={key:{"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size} for key,path in files.items()};(output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8");return {"validated":True,"formats":manifest,"professional_review_required":drawing.professional_review_required}
    def _svg(self,d:Drawing)->str:
        body=[]
        for e in d.entities:
            layer=next(x for x in d.layers if x.name==e.layer)
            if isinstance(e,Line):body.append(f'<line id="{e.entity_id}" x1="{e.x1}" y1="{d.sheet.height_mm-e.y1}" x2="{e.x2}" y2="{d.sheet.height_mm-e.y2}" stroke="{layer.color}" stroke-width="{layer.lineweight_mm}"/>')
            elif isinstance(e,Text):body.append(f'<text id="{e.entity_id}" x="{e.x}" y="{d.sheet.height_mm-e.y}" font-size="{e.height_mm}" transform="rotate({-e.rotation_deg} {e.x} {d.sheet.height_mm-e.y})">{html.escape(e.value)}</text>')
            else:body.extend(self._svg_dimension(e,d.sheet.height_mm,layer.color))
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{d.sheet.width_mm}mm" height="{d.sheet.height_mm}mm" viewBox="0 0 {d.sheet.width_mm} {d.sheet.height_mm}">\n'+"\n".join(body)+"\n</svg>\n"
    def _svg_dimension(self,e:Dimension,height:float,color:str)->list[str]:
        x1,y1,x2,y2,tx,ty,rotation=self._dimension_geometry(e);sy1=height-y1;sy2=height-y2;sty=height-ty
        return [f'<line id="{e.entity_id}" x1="{x1}" y1="{sy1}" x2="{x2}" y2="{sy2}" stroke="{color}" stroke-width="0.18"/>',f'<text x="{tx}" y="{sty}" font-size="2.5" text-anchor="middle" transform="rotate({-rotation} {tx} {sty})">{e.value:g} {html.escape(e.unit)}</text>']
    def _dxf(self,d:Drawing)->str:
        rows=["0","SECTION","2","ENTITIES"]
        for e in d.entities:
            if isinstance(e,Line):rows += ["0","LINE","8",e.layer,"10",str(e.x1),"20",str(e.y1),"11",str(e.x2),"21",str(e.y2)]
            elif isinstance(e,Text):rows += ["0","TEXT","8",e.layer,"10",str(e.x),"20",str(e.y),"40",str(e.height_mm),"1",e.value.encode("ascii","replace").decode()]
            else:
                x1,y1,x2,y2,tx,ty,rotation=self._dimension_geometry(e);rows += ["0","LINE","8",e.layer,"10",str(x1),"20",str(y1),"11",str(x2),"21",str(y2),"0","TEXT","8",e.layer,"10",str(tx),"20",str(ty),"40","2.5","50",str(rotation),"1",f"{e.value:g} {e.unit}"]
        return "\n".join(rows+["0","ENDSEC","0","EOF",""])
    def _pdf(self,d:Drawing)->bytes:
        scale=72/25.4;commands=["0 0 0 RG","0.5 w"]
        for e in d.entities:
            if isinstance(e,Line):commands.append(f"{e.x1*scale:.3f} {e.y1*scale:.3f} m {e.x2*scale:.3f} {e.y2*scale:.3f} l S")
            elif isinstance(e,Text):commands.append(f"BT /F1 {e.height_mm*scale:.3f} Tf {e.x*scale:.3f} {e.y*scale:.3f} Td ({self._pdf_text(e.value)}) Tj ET")
            else:
                x1,y1,x2,y2,tx,ty,rotation=self._dimension_geometry(e);commands.append(f"{x1*scale:.3f} {y1*scale:.3f} m {x2*scale:.3f} {y2*scale:.3f} l S");commands.append(f"BT /F1 {2.5*scale:.3f} Tf {tx*scale:.3f} {ty*scale:.3f} Td ({e.value:g} {self._pdf_text(e.unit)}) Tj ET")
        stream="\n".join(commands).encode("latin-1","replace");objects=[b"<< /Type /Catalog /Pages 2 0 R >>",b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {d.sheet.width_mm*scale:.3f} {d.sheet.height_mm*scale:.3f}] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>".encode(),b"<< /Length "+str(len(stream)).encode()+b" >>\nstream\n"+stream+b"\nendstream",b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
        pdf=bytearray(b"%PDF-1.4\n");offsets=[0]
        for i,obj in enumerate(objects,1):offsets.append(len(pdf));pdf.extend(f"{i} 0 obj\n".encode()+obj+b"\nendobj\n")
        xref=len(pdf);pdf.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode());[pdf.extend(f"{offset:010d} 00000 n \n".encode()) for offset in offsets[1:]];pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode());return bytes(pdf)
    @staticmethod
    def _pdf_text(value):return value.replace("\\","\\\\").replace("(","\\(").replace(")","\\)").encode("latin-1","replace").decode("latin-1")
    @staticmethod
    def _dimension_geometry(e:Dimension):
        if abs(e.x2-e.x1)>=abs(e.y2-e.y1):
            y=e.y1+e.offset_mm;return e.x1,y,e.x2,y,(e.x1+e.x2)/2,y+2,0
        x=e.x1+e.offset_mm;return x,e.y1,x,e.y2,x+2,(e.y1+e.y2)/2,90
