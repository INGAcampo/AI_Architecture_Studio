from pathlib import Path
import json
class ExecutionCheckpoint:
    def __init__(self, plan:str|Path): self.path=Path(plan)
    def run(self):
        if not self.path.exists(): return {'status':'HOLD','reason':'plan absent'}
        p=json.loads(self.path.read_text(encoding='utf-8')); ok=bool(p.get('current')) and bool(p.get('next'))
        return {'status':'CONTINUE' if ok else 'HOLD','reason':'plan coherent' if ok else 'current/next missing'}
