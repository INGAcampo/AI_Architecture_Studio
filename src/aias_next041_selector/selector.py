from pathlib import Path
import json
class NextWorkSelector:
    def __init__(self,plan:str|Path): self.path=Path(plan)
    def select(self):
        if not self.path.exists(): return None
        return json.loads(self.path.read_text(encoding='utf-8')).get('next')
