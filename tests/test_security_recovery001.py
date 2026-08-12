import json,zipfile
from datetime import datetime,timezone,timedelta
from pathlib import Path
import pytest
from aias_security_recovery import BackupManager,SecurityRecoveryPolicy,SecurityScanner
KEY=b"k"*32
def source(tmp_path):
 root=tmp_path/"source";root.mkdir();(root/"model.json").write_text('{"project":"AIAS"}',encoding="utf-8");(root/"nested").mkdir();(root/"nested/data.txt").write_text("engineering",encoding="utf-8");(root/".env").write_text("TOKEN=secret",encoding="utf-8");return root
def test_signed_backup_excludes_secrets_and_verifies(tmp_path):
 manager=BackupManager();result=manager.create(source(tmp_path),tmp_path/"backup.zip","SNP-001",KEY);assert result["verified"] and result["files"]==2 and result["excluded"][0]["path"]==".env" and manager.verify(Path(result["archive"]),KEY)["valid"]
def test_wrong_key_or_tampered_payload_fails_verification(tmp_path):
 manager=BackupManager();archive=tmp_path/"b.zip";manager.create(source(tmp_path),archive,"SNP-002",KEY);assert not manager.verify(archive,b"x"*32)["valid"]
 with pytest.warns(UserWarning,match="Duplicate name"):
  with zipfile.ZipFile(archive,"a") as bundle:bundle.writestr("model.json",b"tampered")
 assert not manager.verify(archive,KEY)["valid"]
def test_safe_restore_and_drill_prove_recoverability(tmp_path):
 manager=BackupManager();archive=tmp_path/"b.zip";manager.create(source(tmp_path),archive,"SNP-003",KEY);result=manager.drill(archive,tmp_path/"drill",KEY);assert result["verified"] and result["restored"]==2 and result["rto_met"] and (tmp_path/"drill/nested/data.txt").read_text()=="engineering"
 with pytest.raises(ValueError,match="not_empty"):manager.restore(archive,tmp_path/"drill",KEY)
def test_scanner_reports_patterns_without_exposing_secret():assert SecurityScanner().scan_text("api_key=SUPERSECRET")==["secret_pattern:1"]
def test_objectives_and_retention_are_measured_without_deletion():
 policy=SecurityRecoveryPolicy(rpo_minutes=60,rto_minutes=2,retention_count=2);now=datetime.now(timezone.utc);status=policy.objective_status((now-timedelta(minutes=30)).isoformat(),30,now);assert status["rpo_met"] and status["rto_met"]
 rows=[{"snapshot_id":f"S{i}","created_at":f"2026-01-0{i}T00:00:00+00:00","verified":True} for i in range(1,5)];assert policy.retention_candidates(rows)==["S2","S1"]
