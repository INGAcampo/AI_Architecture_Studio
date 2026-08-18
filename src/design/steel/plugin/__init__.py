from platform_sdk.plugins import PluginManifest
from design.steel.repositories import *
from design.steel.catalog import seed_default_catalog
from design.steel.design_engine import SteelDesignEngine
from design.steel.optimizer import SteelProfileOptimizer
from design.steel.reports import SteelReportEngine
from design.steel.ai_advisor import SteelAIAdvisor
from design.steel.workspace import SteelWorkspace
class SteelPlatformPlugin:
 manifest=PluginManifest('design.steel','Professional Steel Design','1.0')
 def activate(self,c):
  pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr);d=SteelDesignEngine();c.services.register('steel.profiles',pr,replace=True);c.services.register('steel.materials',mr,replace=True);c.services.register('steel.design',d,replace=True);c.services.register('steel.optimizer',SteelProfileOptimizer(d),replace=True);c.services.register('steel.reports',SteelReportEngine(),replace=True);c.services.register('steel.ai',SteelAIAdvisor(),replace=True);SteelWorkspace().install(c)
