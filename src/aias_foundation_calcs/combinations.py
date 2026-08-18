"""Linear load-case combination with explicit missing-case validation."""
from __future__ import annotations
from .models import LoadCase, LoadCombination

class LoadCombinationEngine:
    """Apply named factors to axial, moment and shear components of load cases."""
    def combine(self, cases: dict[str, LoadCase], combination: LoadCombination) -> LoadCase:
        """Apply factors to every force component after validating case references."""
        missing=[name for name in combination.factors if name not in cases]
        if missing:
            raise KeyError("missing_load_cases:" + ",".join(missing))
        total=LoadCase(combination.name,0.0)
        for name,factor in combination.factors.items():
            c=cases[name]
            total.axial_kn += factor*c.axial_kn
            total.moment_x_knm += factor*c.moment_x_knm
            total.moment_y_knm += factor*c.moment_y_knm
            total.shear_x_kn += factor*c.shear_x_kn
            total.shear_y_kn += factor*c.shear_y_kn
        return total
