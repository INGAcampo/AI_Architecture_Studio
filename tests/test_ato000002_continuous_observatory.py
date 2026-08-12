from datetime import datetime,timezone,timedelta
import pytest
from pathlib import Path
from aias_continuous_observatory import ContinuousObservatory,FeedItem
from aias_continuous_observatory.registry import SourceRegistry
ROOT=Path(__file__).resolve().parents[1];REG=ROOT/"engineering/aias/ato/ATO_CONTINUOUS_SOURCE_REGISTRY.json"
def item(source):return FeedItem(source["id"],"Open engineering advance",source["base_url"]+"advance","2026-08-03","Reusable verified method",source["domains"][0],.95,.9,.9,.8,.1)
def test_cycle_admits_deduplicates_and_recommends(tmp_path):
 o=ContinuousObservatory(SourceRegistry(REG),tmp_path/"ledger.json");now=datetime(2026,8,3,tzinfo=timezone.utc);r=o.run_cycle(lambda s:[item(s)],now);assert r["admitted"]==5 and r["new_recommendations"]==5
 assert sum(len(v) for v in r["radar"].values())==5
 later=now+timedelta(days=15);r2=o.run_cycle(lambda s:[item(s)],later);assert r2["duplicates"]==5 and r2["admitted"]==0
def test_ledger_is_persistent_and_recommendation_contract_complete(tmp_path):
 path=tmp_path/"ledger.json";o=ContinuousObservatory(SourceRegistry(REG),path);o.run_cycle(lambda s:[item(s)],datetime(2026,8,3,tzinfo=timezone.utc));restored=ContinuousObservatory(SourceRegistry(REG),path);rec=restored.ledger["recommendations"][0];assert {"observation","evidence","expected_benefit","cost_and_tradeoffs","risk","recommended_action","urgency"}<=set(rec)
def test_host_allowlist_blocks_untrusted_items(tmp_path):
 o=ContinuousObservatory(SourceRegistry(REG),tmp_path/"ledger.json")
 def bad(source):return [FeedItem(source["id"],"bad","https://evil.example/x","2026","x","x",.9,.9,.9,.9,.1)]
 with pytest.raises(ValueError,match="source_host_not_allowed"):o.run_cycle(bad,datetime(2026,8,3,tzinfo=timezone.utc))
def test_cadence_prevents_early_repoll(tmp_path):
 o=ContinuousObservatory(SourceRegistry(REG),tmp_path/"ledger.json");now=datetime(2026,8,3,tzinfo=timezone.utc);o.run_cycle(lambda s:[],now);assert o.due_sources(now+timedelta(hours=1))==()
def test_cli_materializes_scheduled_cycle(tmp_path):
 import json,subprocess,sys,os
 source=SourceRegistry(REG).sources["SRC-NIST"];row=item(source);batch=tmp_path/"batch.json";batch.write_text(json.dumps({"SRC-NIST":[{k:v for k,v in row.to_dict().items() if k!="fingerprint"}]}),encoding="utf-8");ledger=tmp_path/"ledger.json";env=dict(os.environ);env["PYTHONPATH"]=str(ROOT/"src");result=subprocess.run([sys.executable,"-m","aias_continuous_observatory.cli","--registry",str(REG),"--ledger",str(ledger),"--batch",str(batch),"--now","2026-08-03T00:00:00+00:00"],cwd=ROOT,env=env,capture_output=True,text=True);assert result.returncode==0,result.stderr;assert json.loads(ledger.read_text(encoding="utf-8"))["cycles"][0]["admitted"]==1
