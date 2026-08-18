"""Structured descriptive-memory generation and dependency-free PDF writing."""
from __future__ import annotations
import json,textwrap
from pathlib import Path
from .models import ProjectBrief

def build_memory(brief:ProjectBrief,engineering:dict,drawings:dict)->dict:
    """Build a descriptive memory from explicit project and validated-engine evidence."""
    brief.validate();return {"document_id":f"MEM-{brief.project_id}-{brief.revision}","title":"MEMORIA DESCRIPTIVA","project":{"id":brief.project_id,"title":brief.title,"location":brief.location,"client":brief.client,"discipline":brief.discipline,"scope":brief.scope},"revision":brief.revision,"prepared_by":brief.prepared_by,"checked_by":brief.checked_by,"sections":[{"heading":"1. Objeto","body":f"Documentar el alcance tecnico de {brief.title}."},{"heading":"2. Alcance","body":brief.scope},{"heading":"3. Metodologia","body":"Flujo guiado por especificaciones con calculo, verificacion, dibujo y evidencia encadenada."},{"heading":"4. Resultados","body":f"Calculo validado: {engineering['calculation']['validated']}. Verificacion validada: {engineering['code_checks']['validated']}. Formatos de plano: {', '.join(sorted(drawings['formats']))}."},{"heading":"5. Limitaciones","body":"Documento de referencia. Requiere normativa oficial aplicable, revision y firma de profesional habilitado antes de uso regulado o constructivo."}],"legal_status":"FOR_REVIEW","professional_review_required":True}
def write_memory(memory:dict,output:Path)->dict:
    """Write JSON, Markdown and a renderable text PDF for the descriptive memory."""
    output.mkdir(parents=True,exist_ok=True);json_path=output/"MEMORIA_DESCRIPTIVA.json";md_path=output/"MEMORIA_DESCRIPTIVA.md";pdf_path=output/"MEMORIA_DESCRIPTIVA.pdf";json_path.write_text(json.dumps(memory,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=[f"# {memory['title']}","",f"Proyecto: {memory['project']['title']}",f"Ubicacion: {memory['project']['location']}",f"Revision: {memory['revision']}",f"Estado: {memory['legal_status']}",""]
    for section in memory["sections"]:lines += [f"## {section['heading']}","",section["body"],""]
    md_path.write_text("\n".join(lines),encoding="utf-8");pdf_path.write_bytes(_pdf(lines));return {"json":str(json_path),"markdown":str(md_path),"pdf":str(pdf_path)}
def _pdf(lines:list[str])->bytes:
    wrapped=[]
    for line in lines:wrapped.extend(textwrap.wrap(line.replace("#","").strip(),95) or [""])
    commands=["BT /F1 11 Tf 50 790 Td"]
    for line in wrapped[:52]:commands.append(f"({escape(line)}) Tj 0 -14 Td")
    commands.append("ET");stream="\n".join(commands).encode("latin-1","replace");objects=[b"<< /Type /Catalog /Pages 2 0 R >>",b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",b"<< /Length "+str(len(stream)).encode()+b" >>\nstream\n"+stream+b"\nendstream",b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    pdf=bytearray(b"%PDF-1.4\n");offsets=[]
    for i,obj in enumerate(objects,1):offsets.append(len(pdf));pdf.extend(f"{i} 0 obj\n".encode()+obj+b"\nendobj\n")
    xref=len(pdf);pdf.extend(f"xref\n0 6\n0000000000 65535 f \n".encode());[pdf.extend(f"{o:010d} 00000 n \n".encode()) for o in offsets];pdf.extend(f"trailer << /Size 6 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode());return bytes(pdf)
def escape(value):
    """Escape text for safe inclusion in the generated PDF content stream."""
    return value.encode("latin-1","replace").decode("latin-1").replace("\\","\\\\").replace("(","\\(").replace(")","\\)")
