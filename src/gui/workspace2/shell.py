"""Framework-neutral state contract for the Workspace 2.0 application shell."""
from __future__ import annotations

from dataclasses import dataclass, field


REGIONS = ("top", "left", "center", "right", "bottom", "overlay")
PROFILES = ("Architecture", "Structure", "Geotechnics", "Civil and Survey", "MEP", "Coordination", "Construction", "Learning")


@dataclass(frozen=True)
class ShellProfile:
    name: str
    visible_regions: tuple[str, ...] = REGIONS

    def __post_init__(self):
        if self.name not in PROFILES:
            raise ValueError(f"unsupported_workspace_profile:{self.name}")
        unknown = set(self.visible_regions) - set(REGIONS)
        if unknown:
            raise ValueError(f"unsupported_shell_regions:{sorted(unknown)}")


@dataclass
class Workspace2Shell:
    profile: ShellProfile = field(default_factory=lambda: ShellProfile("Architecture"))
    theme: str = "dark"
    jurisdiction: str = "VE"
    review_status: str = "DRAFT"

    def set_theme(self, theme: str) -> None:
        if theme not in {"dark", "light"}:
            raise ValueError("unsupported_theme")
        self.theme = theme

    def switch_profile(self, name: str) -> None:
        self.profile = ShellProfile(name)

    def snapshot(self) -> dict:
        return {
            "schema": "AIAS-WORKSPACE-2-SHELL-1.0",
            "profile": self.profile.name,
            "visible_regions": list(self.profile.visible_regions),
            "theme": self.theme,
            "jurisdiction": self.jurisdiction,
            "review_status": self.review_status,
        }
