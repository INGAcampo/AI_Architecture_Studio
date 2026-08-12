import json
from aias_next059_selector import NextMacrodelivery
def test_selects_next(tmp_path):
 p=tmp_path/'p';p.write_text(json.dumps({'next':'X'}));assert NextMacrodelivery(p).select()=='X'
