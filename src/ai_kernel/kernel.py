from .population import PopulationManager
from .metrics import MetricsEngine
from .plugins import OptimizerPluginRegistry

class AIGenerativeKernel:
    def __init__(self, evaluation_pipeline):
        self.population = PopulationManager()
        self.metrics = MetricsEngine()
        self.plugins = OptimizerPluginRegistry()
        self.evaluation_pipeline = evaluation_pipeline
        self._reports = []

    def add_candidate(self, candidate):
        self.population.add(candidate)

    def evaluate_all(self):
        self._reports = [
            self.evaluation_pipeline.evaluate(candidate)
            for candidate in self.population.all()
        ]
        return tuple(self._reports)

    def metrics_snapshot(self):
        return self.metrics.summarize(self._reports)

    def run_plugin(self, plugin_id):
        plugin = self.plugins.get(plugin_id)
        return plugin.optimize(self, self.population)
