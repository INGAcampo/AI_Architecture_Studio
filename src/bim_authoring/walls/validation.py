from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WallIssue:
    code: str
    severity: str
    wall_id: str
    message: str

class WallValidator:
    def validate(self, wall, openings=()):
        issues = []
        if wall.profile.height < 2.0:
            issues.append(WallIssue("low_height", "warning", wall.wall_id, "Altura menor a 2.0 m"))
        if wall.wall_type.structure.total_thickness < 0.08:
            issues.append(WallIssue("thin_wall", "warning", wall.wall_id, "Espesor menor a 0.08 m"))
        for opening in openings:
            if opening.offset + opening.width > wall.profile.length:
                issues.append(WallIssue("opening_outside", "error", wall.wall_id, opening.opening_id))
        return tuple(issues)
