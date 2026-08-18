"""Public module supporting AEPS repeatable generation and delivery automation."""
class SpecificationCompiler:
    """Execute the public SpecificationCompiler operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    def to_ir(self,s):
        """Project the current value into the stable ir representation."""
        return {'id':s.specification_id,'module':s.module_name,'version':s.version,
        'contracts':[{'requirement_id':r['id'],'statement':r['statement'],'acceptance_criteria':list(r.get('acceptance_criteria',[]))} for r in s.requirements],
        'dependencies':list(s.dependencies),'architecture_refs':list(s.architecture_refs),'adr_refs':list(s.adr_refs)}
