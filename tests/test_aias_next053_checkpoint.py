from aias_next053_checkpoint import StrategicContinuityCheckpoint
def test_checkpoint_holds(tmp_path):assert StrategicContinuityCheckpoint(tmp_path).run()['status']=='HOLD'
