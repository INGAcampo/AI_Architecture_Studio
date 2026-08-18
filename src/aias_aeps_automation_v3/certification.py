"""Public module supporting AEPS repeatable generation and delivery automation."""
from pathlib import Path
import json,time
class CertificationEngine:
    """Execute the public CertificationEngine operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    def certify(self,spec_id,ws,issues):
        """Execute the public CertificationEngine.certify operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
        d=ws/'certification'; d.mkdir(parents=True,exist_ok=True); p=d/'certificate.json'; certified=not issues
        p.write_text(json.dumps({'specification_id':spec_id,'certified':certified,'issues':issues,'timestamp':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},indent=2),encoding='utf-8')
        return {'certified':certified,'path':p,'issues':tuple(issues)}
