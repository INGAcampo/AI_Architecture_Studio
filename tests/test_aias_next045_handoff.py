import json
from aias_next045_handoff import RoadmapHandoff
def test_handoff_contains_next(tmp_path):
 p=tmp_path/'p';p.write_text(json.dumps({'current':'A','next':'B'}));assert RoadmapHandoff(p).build()['next']=='B'
