from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckpointToken:
    canonical_head:str
    tracked_staged_count:int
    tracked_unstaged_count:int
    desktop_paused:bool
    scheduled_writer_paused:bool

def validate_checkpoint_token(token:CheckpointToken):
    if len(token.canonical_head)!=40:
        return False,"invalid_head"
    if token.tracked_staged_count!=0:
        return False,"staged_changes_present"
    if token.tracked_unstaged_count!=0:
        return False,"unstaged_changes_present"
    if not token.desktop_paused:
        return False,"desktop_not_paused"
    if not token.scheduled_writer_paused:
        return False,"scheduled_writer_not_paused"
    return True,"accepted"
