from __future__ import annotations
import json
from pathlib import Path
from gui.workspace2 import CoordinationLearningHub,render_coordination_learning
def main():
 root=Path(__file__).resolve().parents[1];data=CoordinationLearningHub(root).build_lighthouse();out=root/"workspace2_w2_06_outputs";out.mkdir(parents=True,exist_ok=True);(out/"COORDINATION_LEARNING.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");(out/"COORDINATION_LEARNING.html").write_text(render_coordination_learning(data),encoding="utf-8");print(out)
if __name__=="__main__":main()
