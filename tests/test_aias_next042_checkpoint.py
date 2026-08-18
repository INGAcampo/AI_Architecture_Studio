from aias_next042_checkpoint import ExecutionCheckpoint

def test_holds_missing_plan(tmp_path):
    assert ExecutionCheckpoint(tmp_path/'x').run()['status']=='HOLD'
