"""Structural load-case and linear combination contracts."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LoadCase:
    """Named collection of structural load components."""
    name: str
    nodal_loads: tuple

@dataclass(frozen=True, slots=True)
class LoadCombination:
    """Named factor mapping referencing registered load cases."""
    name: str
    factors: dict

class LoadCombinationEngine:
    """Combine load components while rejecting unknown case references."""
    def combine_nodal_loads(self, cases, combination):
        """Execute the public LoadCombinationEngine.combine_nodal_loads operation for the Omega structural analysis and design suite using explicit caller inputs."""
        by = {c.name: c for c in cases}
        acc = {}
        for case_name, factor in combination.factors.items():
            case = by[case_name]
            for load in case.nodal_loads:
                row = acc.setdefault(load.node_id, [0.0,0.0,0.0])
                row[0] += factor * load.fx_n
                row[1] += factor * load.fy_n
                row[2] += factor * load.mz_nm
        from .model import NodalLoad2D
        return tuple(NodalLoad2D(node_id, *values) for node_id, values in acc.items())
