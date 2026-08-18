from __future__ import annotations
from pathlib import Path
import hashlib, json

class ExchangeWriters:
    """Controlled text DXF and minimal multipage PDF writers; no false DWG claim."""
    def write_dxf(self, cad, path: str | Path) -> dict:
        lines=["0","SECTION","2","HEADER","0","ENDSEC","0","SECTION","2","ENTITIES"]
        for e in cad.entities:
            kind=e["kind"]; geo=e["geometry"]
            if kind in {"line","dimension"} and isinstance(geo,list) and len(geo)>=2:
                a,b=geo[0],geo[1]; lines += ["0","LINE","8",e["layer"],"10",str(a[0]),"20",str(a[1]),"11",str(b[0]),"21",str(b[1])]
            elif kind in {"polyline","rectangle"}:
                lines += ["0","LWPOLYLINE","8",e["layer"],"90",str(len(geo))]
                for p in geo: lines += ["10",str(p[0]),"20",str(p[1])]
            elif kind in {"text","level","bubble"}: lines += ["0","TEXT","8",e["layer"],"1",str(e.get("attributes",{}).get("text",e.get("attributes",{}).get("label",""))),"10","0","20","0"]
        lines += ["0","ENDSEC","0","EOF"]
        payload="\n".join(lines)+"\n"; Path(path).write_text(payload,encoding="ascii"); return {"format":"DXF_ASCII","entities":payload.count("\n0\n"),"sha256":sha(payload)}

    def write_pdf(self, cad, path: str | Path) -> dict:
        pages=[]
        for sheet in cad.sheets:
            text=f"AIAS | {sheet['number']} | {sheet['title']} | Scale {sheet['scale']}"
            stream=f"BT /F1 12 Tf 50 780 Td ({text}) Tj 0 -24 Td (Project: {cad.project_id}) Tj ET".encode("ascii","replace"); pages.append(stream)
        objs=[]; objs.append("<< /Type /Catalog /Pages 2 0 R >>"); objs.append(f"<< /Type /Pages /Kids [{' '.join(f'{4+i*2} 0 R' for i in range(len(pages)))}] /Count {len(pages)} >>"); objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        for i,s in enumerate(pages): objs += [f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 842 595] /Resources << /Font << /F1 3 0 R >> >> /Contents {5+i*2} 0 R >>",f"<< /Length {len(s)} >>\nstream\n{s.decode()}\nendstream"]
        out=b"%PDF-1.4\n"; offsets=[]
        for i,o in enumerate(objs,1): offsets.append(len(out)); out+=f"{i} 0 obj\n{o}\nendobj\n".encode()
        xref=len(out); out+=f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()+b"".join(f"{x:010d} 00000 n \n".encode() for x in offsets)+f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode(); Path(path).write_bytes(out); return {"format":"PDF","pages":len(pages),"sha256":sha(out)}

def sha(value):
    if isinstance(value,str): value=value.encode()
    return hashlib.sha256(value).hexdigest()
