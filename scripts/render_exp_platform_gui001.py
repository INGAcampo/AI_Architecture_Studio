from pathlib import Path
from gui.workspace2 import CapabilityCenter, render_capability_center
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"exp_platform_gui001_outputs";OUT.mkdir(exist_ok=True);snapshot=CapabilityCenter(ROOT).snapshot();(OUT/"CAPABILITY_CENTER.html").write_text(render_capability_center(snapshot),encoding="utf-8");import json;(OUT/"CAPABILITY_CENTER_SNAPSHOT.json").write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(OUT/"CAPABILITY_CENTER.html")
