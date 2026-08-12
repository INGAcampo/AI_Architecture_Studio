import json
from aias_next041_selector import NextWorkSelector
def test_selects_declared_next(tmp_path):
 p=tmp_path/'p.json';p.write_text(json.dumps({'next':'X'}));assert NextWorkSelector(p).select()=='X'
