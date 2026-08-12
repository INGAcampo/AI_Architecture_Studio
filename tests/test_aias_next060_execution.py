from aias_next060_execution import ExecutionContinuation
def test_execution_holds_missing(tmp_path):assert ExecutionContinuation(tmp_path/'x').check()['status']=='HOLD'
