from pathlib import Path
import json
from aias_distribution import OfflineMediaBuilder
ROOT=Path(__file__).resolve().parents[1]
NAMES=("AIAS_DESIGN_SYSTEM001_EXPERIENCE_FOUNDATION_INSTALLER","AIAS_WORKSPACE2_W2_04_COMMAND_STATUS_INSTALLER","AIAS_WORKSPACE2_W2_05_LIGHTHOUSE_JOURNEY_INSTALLER","AIAS_WORKSPACE2_W2_06_COORDINATION_LEARNING_INSTALLER","AIAS_WORKSPACE2_W2_07_VALIDATION_CAMPAIGN_INSTALLER","AIAS_SECURITY_RECOVERY001_VERIFIABLE_RECOVERY_INSTALLER","AIAS_GOV_CONTINUITY001_VERIFIABLE_HANDOFF_INSTALLER")
if __name__=="__main__":
 output=ROOT/"exp_installer_iso001_outputs";output.mkdir(parents=True,exist_ok=True);result=OfflineMediaBuilder().build(ROOT,NAMES,output/"AIAS_INTERNAL_OFFLINE_MEDIA_1.0.0.zip","1.0.0");(output/"OFFLINE_MEDIA_BUILD_REPORT.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8");print(json.dumps(result,indent=2))
