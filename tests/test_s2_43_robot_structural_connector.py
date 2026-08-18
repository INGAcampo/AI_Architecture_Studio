import pytest
from engines.structural.robot_connector import *
@pytest.mark.parametrize("index",range(120))
def test_robot_connector(index):
    c=RobotStructuralConnector();b=RobotBar(f"B{index}","N1","N2","IPE300","S355")
    assert c.import_json(c.export_json((b,)))[0]==b
