"""AST-based translated-key and hard-coded GUI string coverage audit."""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path

class I18nCoverageAuditor:
    """Measure source evidence without claiming complete language coverage."""
    def audit(self,root:Path)->dict:
        root=root.resolve();files=sorted((root/"src/gui").rglob("*.py"));candidates=[];keys=[]
        catalogs=[];catalog_keys=set()
        for catalog_path in sorted((root/"resources/i18n").glob("*.json")):
            try:payload=json.loads(catalog_path.read_text(encoding="utf-8"))
            except (OSError,json.JSONDecodeError):continue
            catalogs.append(payload.get("locale",catalog_path.stem));catalog_keys.update(payload.get("messages",{}))
        for path in files:
            try:tree=ast.parse(path.read_text(encoding="utf-8"))
            except (OSError,SyntaxError,UnicodeDecodeError):continue
            relative=path.relative_to(root).as_posix()
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="translate" and node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):keys.append({"file":relative,"line":node.lineno,"key":node.args[0].value})
                if isinstance(node,ast.Constant) and isinstance(node.value,str):
                    if node.value in catalog_keys:keys.append({"file":relative,"line":getattr(node,"lineno",0),"key":node.value,"reference":"CATALOG_KEY_LITERAL"})
                    if self._candidate(node.value):candidates.append({"file":relative,"line":getattr(node,"lineno",0),"text_sha256":hashlib.sha256(node.value.encode()).hexdigest(),"preview":node.value[:80]})
        unique_references=sorted({item["key"] for item in keys})
        payload={"audit_id":"I18N-CORE-001","status":"GAPS_RECORDED","files_scanned":len(files),"catalog_locales":sorted(set(catalogs)),"catalog_keys":len(catalog_keys),"hardcoded_candidates":len(candidates),"translation_key_references":len(unique_references),"referenced_keys":unique_references,"translation_keys":keys,"candidate_samples":candidates[:100],"full_gui_translation_claimed":False}
        payload["sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();return payload
    @staticmethod
    def _candidate(text:str)->bool:
        value=" ".join(text.split())
        if len(value)<4 or len(value)>300 or "<html" in value.lower() or "{" in value or "}" in value:return False
        if value.startswith(("AIAS-","http","src/","engineering/")):return False
        return any(character.isalpha() for character in value) and (" " in value or any(ord(character)>127 for character in value))
    def write(self,root:Path,output:Path)->dict:
        report=self.audit(root);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return report
