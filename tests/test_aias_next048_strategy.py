import json
from aias_next048_strategy import StrategicSelector
def test_excludes_deferred(tmp_path):
 p=tmp_path/'p';p.write_text(json.dumps({'backlog':['DEFERRED:X','Y']}));assert StrategicSelector(p).select()['item']=='Y'
