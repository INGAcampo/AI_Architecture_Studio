from dataclasses import dataclass
from platform_sdk.context import PlatformContext
from platform_sdk.analysis_workspace import AnalysisWorkspace
@dataclass(frozen=True,slots=True)
class BootstrapResult:
    context:PlatformContext; installed:tuple[str,...]
class PlatformBootstrap:
    def build(self):
        c=PlatformContext.create_default(); AnalysisWorkspace().install(c)
        c.services.register("platform.context",c)
        return BootstrapResult(c,("analysis_workspace","platform_context"))
