from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RenderBatch:
    batch_id: str
    object_count: int
    triangle_count: int

class MassVisualizationFoundation:
    def total_objects(self, batches):
        return sum(b.object_count for b in batches)

    def total_triangles(self, batches):
        return sum(b.triangle_count for b in batches)
