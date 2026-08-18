"""Public module supporting AEPS repeatable generation and delivery automation."""
from pathlib import Path
import zipfile,json,hashlib
class ReleaseBuilder:
    """Execute the public ReleaseBuilder operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    def build(self,ws,spec_id,version):
        """Build the build required by AEPS repeatable generation and delivery automation from explicit inputs."""
        d=ws/'release'; d.mkdir(parents=True,exist_ok=True); zpath=d/f'{spec_id}_{version}.zip'
        with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
            for p in ws.rglob('*'):
                if p.is_file() and d not in p.parents: z.write(p,p.relative_to(ws))
        sha=hashlib.sha256(zpath.read_bytes()).hexdigest(); m=d/'manifest.json'; m.write_text(json.dumps({'specification_id':spec_id,'version':version,'archive':zpath.name,'sha256':sha},indent=2),encoding='utf-8')
        return {'archive':zpath,'manifest':m,'sha256':sha}
