from pathlib import Path
from aias_structural_codes_program import CoordinationDashboardEngine,CoordinationInterface,CoordinationIssue,DisciplineStatus,REQUIRED_DISCIPLINES
H="a"*64
def disciplines():return tuple(DisciplineStatus(x,f"{x}-MODEL","R1",H,"VALIDATED",0) for x in sorted(REQUIRED_DISCIPLINES))
def test_complete_snapshot_reaches_professional_gate(tmp_path):
 s=CoordinationDashboardEngine().build("P1","R1",disciplines(),(CoordinationInterface("I1","STRUCTURAL","BIM","RESOLVED","evidence://i1"),),());assert s.release_readiness=="READY_FOR_PROFESSIONAL_RELEASE_GATE" and s.professional_release_required;out=CoordinationDashboardEngine().write(s,tmp_path);assert Path(out["panel"]).is_file()
def test_missing_discipline_and_unresolved_interface_block():
 s=CoordinationDashboardEngine().build("P","R",disciplines()[:-1],(CoordinationInterface("I","STRUCTURAL","BIM","OPEN","evidence://i"),),());assert s.release_readiness=="BLOCKED" and "I:unresolved_interface" in s.blocking_reasons
def test_open_critical_issue_blocks_release():
 s=CoordinationDashboardEngine().build("P","R",disciplines(),(),(CoordinationIssue("C1","STRUCTURAL","CRITICAL","OPEN","Instability","evidence://c1"),));assert "C1:critical_open" in s.blocking_reasons
def test_invalid_hash_and_blocked_discipline_are_visible():
 d=list(disciplines());d[0]=DisciplineStatus(d[0].discipline,"M","R","bad","BLOCKED",1);s=CoordinationDashboardEngine().build("P","R",tuple(d),(),());assert any("invalid_evidence" in x for x in s.blocking_reasons) and any("not_ready" in x for x in s.blocking_reasons)
