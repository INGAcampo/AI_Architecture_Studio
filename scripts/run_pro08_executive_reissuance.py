from pathlib import Path
import json
from aias_executive_reissuance import ExecutiveReissuanceCampaign
root=Path(__file__).resolve().parents[1]; base=root/'engineering/aias/professional_project_production/PRO-08_EXECUTIVE_REISSUANCE'; c=ExecutiveReissuanceCampaign()
discovery=c.backend_discovery([]); (base/'PRO08A_DWG_BACKEND_DISCOVERY.json').write_text(json.dumps(discovery,indent=2),encoding='utf-8')
refresh=c.xlsx_refresh('PRO06-GRAPH-C30-37','PRO05-GRAPH-C25-30')
artifacts=[
 {'output':'Native DWG','status':'BLOCKED','evidence':discovery,'action':'Install or authorize a verifiable native DWG backend'},
 {'output':'Professional PDF','status':'V0_LIMITED','evidence':'PRO03 PDF','action':'Adopt a validated professional rendering/layout backend'},
 {'output':'Constructive Standards Pack','status':'BLOCKED','evidence':'No authenticated rule evidence in canonical registry','action':'Acquire and register authoritative licensed standard evidence'},
 {'output':'Reinforcement detailing','status':'PRELIMINARY','evidence':'PRO04','action':'Re-run only after constructive standards evidence'},
 {'output':'Incremental XLSX','status':'V0_LIMITED','evidence':refresh,'action':'Bind a workbook service to canonical artifact graph'},
 {'output':'BIM/Analysis/Reports','status':'PRODUCTION_READY','evidence':'PRO06','action':''}]
m=c.manifest(artifacts); m['xlsx_refresh']=refresh; m['project_graph_fingerprint']='PRO06-GRAPH-C30-37'; (base/'EXECUTIVE_REISSUANCE_MANIFEST.json').write_text(json.dumps(m,indent=2),encoding='utf-8'); print(json.dumps({'verdict':m['verdict'],'critical':m['critical_blockers']},indent=2))
