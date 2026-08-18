from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WorkflowStep:
    step_id: str
    status: str

class IntegratedInfrastructureWorkflow:
    def is_complete(self, steps):
        return all(step.status == "complete" for step in steps)

    def progress(self, steps):
        steps = tuple(steps)
        return sum(step.status == "complete" for step in steps)/len(steps)
