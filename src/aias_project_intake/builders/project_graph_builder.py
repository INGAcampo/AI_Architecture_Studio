from __future__ import annotations
from aias_building_design_core import BuildingDesignCore

class ParametricProjectGraphBuilder:
    """Builds an isolated BIM graph from validated intake; no shared pilot graph."""
    def build(self, manifest):
        from aias_project_intake import ProjectIntake
        intake=ProjectIntake().validate(manifest); p=intake['program']; core=BuildingDesignCore(); graph=core.create_project(manifest['project_name'],project_id=manifest['project_id'])
        graph.add_node('site','Site',id='site-001',width_m=p['width_m'],length_m=p['length_m'])
        graph.add_node('material','Concrete',id='material-concrete',grade='C25/30')
        for i in range(int(p['levels'])):
            lid=f'level-{i+1:02d}'; graph.add_node('level',f'Level {i+1}',id=lid,elevation_m=i*p['storey_height_m']); graph.relate('site-001','contains',lid)
            graph.add_node('space',f'Floor {i+1}',id=f'space-{i+1:02d}',area_m2=p['width_m']*p['length_m']); graph.relate(lid,'contains',f'space-{i+1:02d}')
            graph.add_node('slab',f'Slab {i+1}',id=f'slab-{i+1:02d}',area_m2=p['width_m']*p['length_m'],thickness_m=0.15); graph.relate(lid,'contains',f'slab-{i+1:02d}')
        graph.add_node('foundation','Foundation',id='foundation-001',volume_m3=p['width_m']*p['length_m']*0.15); graph.relate('site-001','supports','foundation-001')
        errors=core.validate(graph)
        if errors: raise ValueError('; '.join(errors))
        return graph
