from __future__ import annotations
import hashlib, json

class ProjectIntake:
    """Fail-closed project manifest intake, isolated by project and mode."""
    def validate(self, manifest):
        required={'project_id','project_name','mode','scenario_id','building_program'}
        missing=required-set(manifest)
        if missing: raise ValueError('missing intake fields: '+','.join(sorted(missing)))
        program=manifest['building_program']
        for key in ('levels','width_m','length_m','storey_height_m'):
            if key not in program or not isinstance(program[key],(int,float)) or program[key]<=0: raise ValueError('invalid building_program.'+key)
        if manifest['mode']=='PILOT_SYNTHETIC' and not (manifest.get('SYNTHETIC_TEST_DATA') and manifest.get('NOT_FOR_CONSTRUCTION')): raise ValueError('synthetic isolation flags required')
        if manifest['mode']=='REAL_PROJECT' and not manifest.get('authenticated_provenance_sha256'): raise ValueError('authenticated provenance required')
        payload={'project_id':manifest['project_id'],'mode':manifest['mode'],'program':program,'scenario_id':manifest['scenario_id']}
        payload['sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest(); return payload
