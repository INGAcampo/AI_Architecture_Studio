from aias_autonomous_supervisor.supervisor import AIASAutonomousSupervisor
def test_resume_and_single_writer(tmp_path):
 s=AIASAutonomousSupervisor(tmp_path); s._head=lambda:'abc'; first=s.run(); assert first['gate_current']=='TARGET_REACHED'; second=s.run(resume=True); assert second['execution_id']==first['execution_id']; assert s.heartbeat_path.exists() and s.journal_path.exists()
