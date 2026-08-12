from aias_next050_execution import StrategicExecution
def test_execution_not_release(tmp_path): assert StrategicExecution(tmp_path/'x').record('A')['release_approved'] is False
