from aias_next049_readiness import StrategicReadiness
def test_readiness_holds_missing(tmp_path): assert StrategicReadiness(tmp_path/'x').check()['ready'] is False
