"""Coordinated drawings, schedules and quantities for the lighthouse building."""
from __future__ import annotations
import csv,json
from io import StringIO
from pathlib import Path

from .multistory import reference_building


def _svg(title:str,body:str,width:int=1100,height:int=650)->str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/><style>text{{font-family:Arial,sans-serif;fill:#172033}}.title{{font-size:24px;font-weight:bold}}.note{{font-size:13px}}.member{{stroke:#176b87;stroke-width:8}}.grid{{stroke:#9ca8b8;stroke-width:1;stroke-dasharray:6 5}}.node{{fill:#d97706;stroke:#172033;stroke-width:2}}</style><text x="40" y="42" class="title">{title}</text>{body}<text x="40" y="625" class="note">AIAS LIGHTHOUSE-000001 · VENEZUELA VE-001 · REFERENCE_ONLY · NO APROBADO PARA CONSTRUCCION</text></svg>'''


def _csv(headers,rows)->str:
    stream=StringIO(newline="");writer=csv.writer(stream,lineterminator="\n");writer.writerow(headers);writer.writerows(rows);return stream.getvalue()


def generate_structural_documents(target:Path,report:dict)->dict:
    """Generate all documents from the same canonical building/report revision."""
    target.mkdir(parents=True,exist_ok=True);building=reference_building();design={row["member_id"]:row for row in report["design"]["selected_sections"]}
    plan=[]
    for x,label in ((150,"A"),(550,"B"),(950,"C")):
        plan.append(f'<line x1="{x}" y1="90" x2="{x}" y2="560" class="grid"/><text x="{x-6}" y="80">{label}</text><circle cx="{x}" cy="320" r="14" class="node"/>')
    plan.extend(('<line x1="150" y1="320" x2="550" y2="320" class="member"/>','<line x1="550" y1="320" x2="950" y2="320" class="member"/>','<rect x="120" y="290" width="60" height="60" fill="none" stroke="#2f855a" stroke-width="4"/><rect x="520" y="290" width="60" height="60" fill="none" stroke="#2f855a" stroke-width="4"/><rect x="920" y="290" width="60" height="60" fill="none" stroke="#2f855a" stroke-width="4"/>'))
    elevation=[]
    for level,y in ((0,550),(1,410),(2,270),(3,130)):
        elevation.append(f'<line x1="100" y1="{y}" x2="1000" y2="{y}" class="grid"/><text x="45" y="{y+5}">N{level}</text>')
    for x in (150,550,950):
        for y1,y2 in ((550,410),(410,270),(270,130)):elevation.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="member"/>')
    for y in (410,270,130):elevation.extend((f'<line x1="150" y1="{y}" x2="550" y2="{y}" class="member"/>',f'<line x1="550" y1="{y}" x2="950" y2="{y}" class="member"/>'))
    (target/"STRUCTURAL_PLAN.svg").write_text(_svg("PLANTA ESTRUCTURAL DE REFERENCIA",''.join(plan)),encoding="utf-8")
    (target/"STRUCTURAL_ELEVATION.svg").write_text(_svg("ELEVACION ESTRUCTURAL DE REFERENCIA",''.join(elevation)),encoding="utf-8")
    beams=[];columns=[]
    for member in building.members:
        row=design[member.member_id];record=(member.member_id,row["selected_section_id"],f'{row["governing_ratio"]:.3f}',row["status"],"REFERENCE_ONLY")
        (beams if member.kind=="BEAM" else columns).append(record)
    footings=[(f"F-{axis}","1.40","1.40","0.50","REFERENCE_ONLY") for axis in range(3)]
    (target/"BEAM_SCHEDULE.csv").write_text(_csv(("mark","reference_section","utilization","status","legal_status"),beams),encoding="utf-8")
    (target/"COLUMN_SCHEDULE.csv").write_text(_csv(("mark","reference_section","utilization","status","legal_status"),columns),encoding="utf-8")
    (target/"FOUNDATION_SCHEDULE.csv").write_text(_csv(("mark","length_m","width_m","depth_m","legal_status"),footings),encoding="utf-8")
    quantities={"schema":"AIAS-LIGHTHOUSE-QUANTITIES-1.0","revision":"R01","basis":"REFERENCE_GEOMETRY_NOT_FOR_PROCUREMENT","concrete_m3":{"columns":2.592,"beams":6.75,"slabs":18.0,"footings":2.94,"total":30.282},"formwork_m2":{"columns":34.56,"beams":43.2,"slab_soffits":120.0,"footings":8.4,"total":206.16},"reinforcement_estimate_kg":{"basis":"REFERENCE_RATIOS_NOT_DETAILING","columns":414.72,"beams":810.0,"slabs":1620.0,"footings":294.0,"total":3138.72},"construction_approved":False}
    (target/"STRUCTURAL_QUANTITIES.json").write_text(json.dumps(quantities,indent=2)+"\n",encoding="utf-8")
    return {"drawings":2,"schedules":3,"quantities":quantities,"source_revision":"R01","construction_approved":False}
