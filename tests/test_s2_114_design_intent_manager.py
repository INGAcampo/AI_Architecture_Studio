import pytest
from engines.ai.design_intent import *
@pytest.mark.parametrize("i",range(120))
def test_intent(i):
    m=DesignIntentManager();m.register(DesignIntent("clearance","Maintain clearance",10));m.register(DesignIntent("alignment","Maintain alignment",5))
    assert m.ordered()[0].intent_id=="clearance"
    assert m.validate({"clearance":True,"alignment":False})[0].intent_id=="alignment"
