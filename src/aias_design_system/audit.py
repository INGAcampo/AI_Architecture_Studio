"""Static migration audit for legacy UI styling."""
from __future__ import annotations
import re
from pathlib import Path

HEX=re.compile(r"#[0-9a-fA-F]{6}\b")

def audit_python_ui(root:Path)->dict:
    files=[];hardcoded=[];inline=[]
    for path in sorted(root.rglob("*.py")):
        text=path.read_text(encoding="utf-8",errors="replace");relative=path.relative_to(root).as_posix();files.append(relative)
        colors=sorted(set(HEX.findall(text)))
        if colors:hardcoded.append({"file":relative,"colors":colors})
        if ".setStyleSheet(" in text:inline.append(relative)
    return {"schema":"AIAS-DESIGN-MIGRATION-AUDIT-1.0","files_scanned":len(files),"hardcoded_color_files":hardcoded,"inline_stylesheet_files":inline,"migration_required":bool(hardcoded or inline),"target":"render_qss() plus semantic component roles"}
