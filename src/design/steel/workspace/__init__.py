from platform_sdk.workspaces import WorkspaceDefinition
class SteelWorkspace:
 def definition(self): return WorkspaceDefinition('steel','Steel Design',('steel_explorer','steel_materials','steel_properties','steel_unity','steel_optimization','steel_reports','steel_ai'),('steel.assign_profile','steel.design','steel.optimize','steel.report'))
 def install(self,c): c.workspaces.register(self.definition(),replace=True);c.services.register('workspace.steel',self,replace=True);c.workspaces.activate('steel');return self
