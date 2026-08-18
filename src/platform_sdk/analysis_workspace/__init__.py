from platform_sdk.workspaces import WorkspaceDefinition
class AnalysisWorkspace:
    def definition(self):
        return WorkspaceDefinition("analysis","Analysis",("analysis_tree","loads","solver","results","benchmarks"),("analysis.run","analysis.report"))
    def install(self,context):
        context.workspaces.register(self.definition(),replace=True)
        context.services.register("workspace.analysis",self,replace=True)
        return self
