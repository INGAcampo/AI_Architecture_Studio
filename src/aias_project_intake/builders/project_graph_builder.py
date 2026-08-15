from __future__ import annotations
from aias_building_design_core import BuildingDesignCore

class ParametricProjectGraphBuilder:
    """Builds an isolated BIM graph from validated intake; no shared pilot graph."""
    def build(self, manifest):
        from aias_project_intake import ProjectIntake
        intake=ProjectIntake().validate(manifest); p=intake['program']; core=BuildingDesignCore(); graph=core.create_project(manifest['project_name'],project_id=manifest['project_id'])
        width=float(p['width_m']); length=float(p['length_m']); height=float(p['storey_height_m'])
        graph.add_node('site','Site',id='site-001',width_m=width,length_m=length,units='SI')
        graph.add_node('material','Concrete',id='material-concrete',grade='C25/30')
        for axis, coordinate in (('A',0.0),('B',width),('1',0.0),('2',length)):
            grid_id=f'grid-{axis}'; graph.add_node('grid',f'Grid {axis}',id=grid_id,axis=axis,coordinate_m=coordinate); graph.relate('site-001','contains',grid_id)
        for i in range(int(p['levels'])):
            number=i+1; lid=f'level-{number:02d}'; graph.add_node('level',f'Level {number}',id=lid,elevation_m=i*height); graph.relate('site-001','contains',lid)
            space=f'space-{number:02d}'; graph.add_node('space',f'Floor {number}',id=space,area_m2=width*length); graph.relate(lid,'contains',space)
            slab=f'slab-{number:02d}'; graph.add_node('slab',f'Slab {number}',id=slab,area_m2=width*length,thickness_m=0.15); graph.relate(lid,'contains',slab); graph.relate(slab,'uses_material','material-concrete')
            for side, wall_length in (('north',width),('south',width),('east',length),('west',length)):
                wall=f'wall-{number:02d}-{side}'; graph.add_node('wall',f'Wall {number} {side}',id=wall,length_m=wall_length,height_m=height,thickness_m=0.20,exterior=True); graph.relate(lid,'contains',wall); graph.relate(space,'bounded_by',wall)
            for corner in ('A1','A2','B1','B2'):
                column=f'column-{number:02d}-{corner}'; graph.add_node('column',f'Column {number} {corner}',id=column,width_m=0.30,depth_m=0.30,height_m=height); graph.relate(lid,'contains',column); graph.relate(column,'uses_material','material-concrete')
            for edge, beam_length in (('A',width),('B',width),('1',length),('2',length)):
                beam=f'beam-{number:02d}-{edge}'; graph.add_node('beam',f'Beam {number} {edge}',id=beam,length_m=beam_length,width_m=0.30,depth_m=0.50); graph.relate(lid,'contains',beam); graph.relate(beam,'uses_material','material-concrete')
            door=f'door-{number:02d}-01'; window=f'window-{number:02d}-01'; graph.add_node('door',f'Door {number}',id=door,width_m=0.90,height_m=2.10); graph.add_node('window',f'Window {number}',id=window,width_m=1.20,height_m=1.20); graph.relate(f'wall-{number:02d}-south','has_opening',door); graph.relate(f'wall-{number:02d}-north','has_opening',window)
        for corner in ('A1','A2','B1','B2'):
            foundation=f'foundation-{corner}'; graph.add_node('foundation',f'Foundation {corner}',id=foundation,system='isolated',width_m=1.20,length_m=1.20,depth_m=0.40); graph.relate('site-001','supports',foundation); graph.relate(foundation,'uses_material','material-concrete')
        graph.add_node('roof','Roof',id='roof-001',area_m2=width*length); graph.relate(f'level-{int(p["levels"]):02d}','contains','roof-001')
        errors=core.validate(graph)
        if errors: raise ValueError('; '.join(errors))
        return graph
