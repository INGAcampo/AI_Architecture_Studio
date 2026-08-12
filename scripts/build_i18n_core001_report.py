import json
from pathlib import Path
from aias_i18n import I18nCoverageAuditor
ROOT=Path(__file__).resolve().parents[1];report=I18nCoverageAuditor().write(ROOT,ROOT/"engineering/aias/internationalization/I18N_CORE_001_COVERAGE.json");print(json.dumps({"files":report["files_scanned"],"candidates":report["hardcoded_candidates"],"catalog_keys":report["catalog_keys"],"referenced_keys":report["translation_key_references"],"sha256":report["sha256"]}))
