from aec_orchestrator_checkpoint.checkpoint import CheckpointToken,validate_checkpoint_token

def valid():
    return CheckpointToken("a"*40,0,0,True,True)

def test_valid_checkpoint_token_is_accepted():
    assert validate_checkpoint_token(valid())==(True,"accepted")

def test_unstaged_changes_are_rejected():
    t=CheckpointToken("a"*40,0,1,True,True)
    assert validate_checkpoint_token(t)[0] is False

def test_active_desktop_is_rejected():
    t=CheckpointToken("a"*40,0,0,False,True)
    assert validate_checkpoint_token(t)[1]=="desktop_not_paused"
