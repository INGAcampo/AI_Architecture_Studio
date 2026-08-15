"""Deterministic bridge from the canonical Project Graph to native BIM wall geometry."""
from __future__ import annotations

from dataclasses import asdict

from bim_authoring.walls import (
    CompoundStructure, NativeBimWallEngine, WallInstance, WallLayer,
    WallLocationLine, WallOpening, WallProfile, WallType,
)


class NativeBimProjection:
    """Projects graph-owned walls/openings without creating a second source of truth."""

    def materialize(self, graph):
        nodes = {node['id']: node for node in graph.nodes}
        site = next((node for node in graph.nodes if node['type'] == 'site'), None)
        if site is None:
            raise ValueError('site is required for native BIM projection')
        width = float(site['properties'].get('width_m', 0.0))
        length = float(site['properties'].get('length_m', 0.0))
        if width <= 0 or length <= 0:
            raise ValueError('site width_m and length_m are required')
        levels = {node['id']: float(node['properties'].get('elevation_m', node['properties'].get('elevation', 0.0))) for node in graph.nodes if node['type'] == 'level'}
        type_ = WallType('aias-concrete-wall-200', 'AIAS Concrete Wall 200', CompoundStructure((WallLayer('core', 'concrete', 0.20, 'core'),)))
        engine = NativeBimWallEngine(); engine.register_type(type_)
        hosts = {rel['target']: rel['source'] for rel in graph.relationships if rel['relation'] in {'contains', 'hosts'} and rel['source'] in levels}
        wall_results = {}
        for wall in (node for node in graph.nodes if node['type'] == 'wall'):
            props = wall['properties']; level_id = hosts.get(wall['id'])
            if level_id is None:
                raise ValueError(f"wall {wall['id']} has no containing level")
            start, end = self._line(wall['id'], width, length, float(props.get('length_m', 0.0)))
            instance = WallInstance(wall['id'], type_, WallProfile(start, end, levels[level_id], float(props.get('height_m', 0.0))), WallLocationLine.CENTERLINE, level_id=level_id, properties={'graph_id': wall['id']})
            engine.add_wall(instance)
        for rel in graph.relationships:
            if rel['relation'] != 'has_opening' or rel['source'] not in engine.walls:
                continue
            opening = nodes[rel['target']]; props = opening['properties']
            engine.add_opening(WallOpening(opening['id'], rel['source'], offset=0.10, width=float(props['width_m']), sill_height=float(props.get('sill_height_m', 0.0)), height=float(props['height_m']), hosted_element_id=opening['id']))
        for wall_id in sorted(engine.walls):
            result = engine.regenerate(wall_id)
            wall_results[wall_id] = {'geometry': asdict(result.geometry), 'quantities': asdict(result.quantities), 'issues': [asdict(issue) for issue in result.issues]}
        return {'schema': 'aias.native_bim_projection.v1', 'project_id': graph.project_id, 'walls': wall_results, 'traceability': {'source': 'ProjectGraph', 'mapping': {wall_id: wall_id for wall_id in wall_results}}}

    @staticmethod
    def _line(wall_id, width, length, fallback):
        side = wall_id.rsplit('-', 1)[-1]
        lines = {
            'north': ((0.0, length, 0.0), (width, length, 0.0)),
            'south': ((0.0, 0.0, 0.0), (width, 0.0, 0.0)),
            'east': ((width, 0.0, 0.0), (width, length, 0.0)),
            'west': ((0.0, 0.0, 0.0), (0.0, length, 0.0)),
        }
        if side in lines:
            return lines[side]
        if fallback <= 0:
            raise ValueError(f'wall {wall_id} has no valid length')
        return (0.0, 0.0, 0.0), (fallback, 0.0, 0.0)
