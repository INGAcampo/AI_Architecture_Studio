from __future__ import annotations
import json
from pathlib import Path
from gui.workspace2 import LighthouseJourney,render_lighthouse_journey
def main():
 root=Path(__file__).resolve().parents[1];data=LighthouseJourney(root/"lighthouse000001_venezuela_outputs"/"technical_dossier").inspect();output=root/"workspace2_w2_05_outputs";output.mkdir(parents=True,exist_ok=True);(output/"LIGHTHOUSE_JOURNEY.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");(output/"LIGHTHOUSE_JOURNEY.html").write_text(render_lighthouse_journey(data),encoding="utf-8");print(output)
if __name__=="__main__":main()
