from platform_sdk.workspaces import WorkspaceDefinition

class SteelFrameWorkspace:
    WORKSPACE_ID="steel_frame"

    def definition(self):
        return WorkspaceDefinition(
            self.WORKSPACE_ID,
            "Steel Frame",
            ("frame_tree","connectivity","load_paths","batch_design","critical_dashboard","global_optimization","frame_report","frame_ai"),
            ("frame.validate","frame.design","frame.optimize","frame.report"),
        )

    def install(self,context):
        context.workspaces.register(self.definition(),replace=True)
        context.services.register("workspace.steel_frame",self,replace=True)
        context.workspaces.activate(self.WORKSPACE_ID)
        return self
