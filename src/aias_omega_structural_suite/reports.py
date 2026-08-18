"""Structural workflow report and machine-readable evidence generation."""
import json
from pathlib import Path

class StructuralReport:
    """Summarize model, analysis, design checks and professional limitations."""
    def to_dict(self, result):
        """Project the current value into the stable dict representation."""
        return {
            "displacements": result.displacements,
            "reactions": result.reactions,
            "element_forces": {
                k: {
                    "axial_i_n": v.axial_i_n,
                    "shear_i_n": v.shear_i_n,
                    "moment_i_nm": v.moment_i_nm,
                    "axial_j_n": v.axial_j_n,
                    "shear_j_n": v.shear_j_n,
                    "moment_j_nm": v.moment_j_nm,
                } for k,v in result.element_forces.items()
            },
        }

    def export_json(self, result, path: Path):
        """Persist json for the Omega structural analysis and design suite in its stable external representation."""
        path.write_text(json.dumps(self.to_dict(result), indent=2), encoding="utf-8")

    def export_markdown(self, result, path: Path):
        """Persist markdown for the Omega structural analysis and design suite in its stable external representation."""
        rows = ["# AIAS Structural Analysis Report", "", "## Displacements"]
        for nid, values in result.displacements.items():
            rows.append(f"- {nid}: ux={values[0]:.6e}, uy={values[1]:.6e}, rz={values[2]:.6e}")
        rows += ["", "## Reactions"]
        for nid, values in result.reactions.items():
            rows.append(f"- {nid}: Rx={values[0]:.3f}, Ry={values[1]:.3f}, Mz={values[2]:.3f}")
        path.write_text("\n".join(rows), encoding="utf-8")
