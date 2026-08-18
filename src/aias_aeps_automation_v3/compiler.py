"""Public module supporting AEPS repeatable generation and delivery automation."""
import json,re
from pathlib import Path
from .models import CompiledSpecification
ID=re.compile(r"^SPEC-\d{6}$"); SEMVER=re.compile(r"^\d+\.\d+\.\d+$")
class EngineeringCompiler:
    """Execute the public EngineeringCompiler operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    def compile_dict(self,d):
        """Execute the public EngineeringCompiler.compile_dict operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
        for k in ('id','title','module_name','version','requirements'):
            if k not in d: raise ValueError(f'Missing field: {k}')
        if not ID.fullmatch(d['id']): raise ValueError('Invalid specification id')
        if not SEMVER.fullmatch(d['version']): raise ValueError('Invalid version')
        if not d['requirements']: raise ValueError('Requirements required')
        return CompiledSpecification(d['id'],d['title'],d['module_name'],d['version'],list(d['requirements']),list(d.get('dependencies',[])),list(d.get('architecture_refs',[])),list(d.get('adr_refs',[])))
    def compile_file(self,path:Path):
        """Read a specification JSON file and compile it into validated intermediate form."""
        return self.compile_dict(json.loads(path.read_text(encoding='utf-8')))
