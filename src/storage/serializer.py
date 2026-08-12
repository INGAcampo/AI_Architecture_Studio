from dataclasses import asdict,is_dataclass
from datetime import datetime,timezone
from pathlib import Path
import json,zipfile
from .checksum import calculate_checksum
from .file_version import AIAS_FILE_VERSION
class ProjectSerializer:
    METADATA_FILE="metadata.json"; DRAWING_FILE="drawing.json"; SETTINGS_FILE="settings.json"; MANIFEST_FILE="manifest.json"
    @staticmethod
    def _ready(v):
        if is_dataclass(v): return asdict(v)
        if hasattr(v,"to_dict") and callable(v.to_dict): return v.to_dict()
        if isinstance(v,dict): return {str(k):ProjectSerializer._ready(x) for k,x in v.items()}
        if isinstance(v,(list,tuple)): return [ProjectSerializer._ready(x) for x in v]
        if isinstance(v,Path): return str(v)
        return v
    def serialize(self,document,destination):
        destination=Path(destination)
        if destination.suffix.lower()!='.aias': destination=destination.with_suffix('.aias')
        destination.parent.mkdir(parents=True,exist_ok=True)
        payloads={self.METADATA_FILE:self._ready(document.metadata),self.DRAWING_FILE:{"objects":self._ready(document.objects),"layers":self._ready(document.layers),"camera":self._ready(document.camera),"custom_data":self._ready(document.custom_data)},self.SETTINGS_FILE:self._ready(document.settings)}
        manifest={"format":"AIAS","file_version":AIAS_FILE_VERSION,"created_utc":datetime.now(timezone.utc).isoformat(),"checksums":{n:calculate_checksum(p) for n,p in payloads.items()}}
        temp=destination.with_suffix(destination.suffix+'.tmp')
        try:
            with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
                for n,p in payloads.items(): z.writestr(n,json.dumps(p,ensure_ascii=False,indent=2))
                z.writestr(self.MANIFEST_FILE,json.dumps(manifest,ensure_ascii=False,indent=2))
                for folder in ('materials','textures','xrefs','thumbnails'): z.writestr(folder+'/.keep','')
            temp.replace(destination)
        except Exception:
            if temp.exists(): temp.unlink()
            raise
        document.file_path=destination; document.mark_clean(); return destination
