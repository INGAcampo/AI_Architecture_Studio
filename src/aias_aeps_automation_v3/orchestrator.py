"""Public module supporting AEPS repeatable generation and delivery automation."""
from .compiler import EngineeringCompiler
from .graph import DependencyGraph
from .specification import SpecificationCompiler
from .generators import CodeGenerationEngine,TestGenerationEngine,DocumentationGenerationEngine
from .validation import ValidationEngine
from .certification import CertificationEngine
from .release import ReleaseBuilder
from .models import PipelineContext,BuildArtifact
class AutomationOrchestrator:
    """Execute the public AutomationOrchestrator operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    def build(self,spec_file,ws):
        """Build the build required by AEPS repeatable generation and delivery automation from explicit inputs."""
        spec=EngineeringCompiler().compile_file(spec_file); ws.mkdir(parents=True,exist_ok=True); ctx=PipelineContext(spec,ws)
        g=DependencyGraph(); g.add_node(spec.specification_id)
        for d in spec.dependencies: g.add_edge(spec.specification_id,d)
        ctx.reports['dependency_order']=g.topological_order(); ir=SpecificationCompiler().to_ir(spec); ctx.reports['ir']=ir
        for engine in (CodeGenerationEngine(),TestGenerationEngine(),DocumentationGenerationEngine()): ctx.artifacts.extend(engine.generate(ir,ws))
        v=ValidationEngine(); issues=v.validate_ir(ir)+v.validate_workspace(ws); ctx.reports['validation_issues']=issues
        cert=CertificationEngine().certify(spec.specification_id,ws,issues); ctx.reports['certified']=cert['certified']; ctx.artifacts.append(BuildArtifact('certificate',cert['path'],spec.specification_id))
        if cert['certified']: ctx.reports['release']={k:str(v) for k,v in ReleaseBuilder().build(ws,spec.specification_id,spec.version).items()}
        return ctx
