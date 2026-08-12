from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WindowIssue:
    code: str
    severity: str
    window_id: str
    message: str

class WindowValidator:
    def validate(self, window, wall=None):
        issues = []
        if window.window_type.width < 0.40:
            issues.append(WindowIssue("narrow_window", "warning", window.window_id, "Ancho menor a 0.40 m"))
        if window.window_type.height < 0.40:
            issues.append(WindowIssue("low_window", "warning", window.window_id, "Altura menor a 0.40 m"))
        if wall is not None:
            if window.offset + window.window_type.width > wall.profile.length:
                issues.append(WindowIssue("outside_host", "error", window.window_id, "La ventana excede el muro"))
            if window.sill_height + window.window_type.height > wall.profile.height:
                issues.append(WindowIssue("too_tall_for_host", "error", window.window_id, "La ventana excede la altura del muro"))
        return tuple(issues)
