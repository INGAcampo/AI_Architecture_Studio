from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DoorIssue:
    code: str
    severity: str
    door_id: str
    message: str

class DoorValidator:
    def validate(self, door, wall=None):
        issues = []
        if door.door_type.width < 0.80:
            issues.append(DoorIssue("narrow_door", "warning", door.door_id, "Ancho menor a 0.80 m"))
        if door.door_type.height < 2.00:
            issues.append(DoorIssue("low_door", "warning", door.door_id, "Altura menor a 2.00 m"))
        if wall is not None:
            if door.offset + door.door_type.width > wall.profile.length:
                issues.append(DoorIssue("outside_host", "error", door.door_id, "La puerta excede el muro"))
            if door.sill_height + door.door_type.height > wall.profile.height:
                issues.append(DoorIssue("too_tall_for_host", "error", door.door_id, "La puerta excede la altura del muro"))
        return tuple(issues)
