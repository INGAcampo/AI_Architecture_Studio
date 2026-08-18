"""Gestor persistente de normas del proyecto AIAS."""

import json
from pathlib import Path

from core.standards.standard_profile import StandardProfile
from core.standards.standard_registry import StandardRegistry
from core.standards.standard_validator import StandardValidator


class StandardManager:

    _instance = None

    def __init__(self, config_path=None):
        self.config_path = Path(
            config_path or "config/standard_settings.json"
        )
        self.active_profile = StandardRegistry.get("venezuela")
        self.load()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_profile(self, profile):
        if profile is None:
            return False
        self.active_profile = profile
        self.save()
        return True

    def set_profile_by_id(self, profile_id):
        profile = StandardRegistry.get(profile_id)
        return self.set_profile(profile)

    def update_active(self, **changes):
        if self.active_profile is None:
            return False

        for key, value in changes.items():
            if hasattr(self.active_profile, key):
                setattr(self.active_profile, key, value)

        self.save()
        return True

    def validate(self):
        return StandardValidator.validate(self.active_profile)

    def save(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "active_profile": self.active_profile.to_dict(),
            "standards_core": "5.2.0",
        }
        self.config_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def load(self):
        if not self.config_path.exists():
            self.save()
            return

        try:
            payload = json.loads(
                self.config_path.read_text(encoding="utf-8")
            )
            data = payload.get("active_profile", {})
            self.active_profile = StandardProfile.from_dict(data)
        except Exception:
            self.active_profile = StandardRegistry.get("venezuela")
            self.save()

    def report(self):
        profile = self.active_profile
        validation = self.validate()

        lines = [
            "AIAS STANDARDS CORE 5.2.0",
            "-" * 78,
        ]

        for key, value in profile.summary().items():
            lines.append(f"{key:<24}: {value}")

        lines.append("-" * 78)
        lines.append(
            f"Estado mínimo: "
            f"{'VÁLIDO' if validation['valid'] else 'INCOMPLETO'}"
        )

        for warning in validation["warnings"]:
            lines.append(f"ADVERTENCIA: {warning}")

        for error in validation["errors"]:
            lines.append(f"ERROR: {error}")

        lines.append(
            "NOTA: AIAS no sustituye la revisión ni la firma del "
            "profesional responsable."
        )
        return "\n".join(lines)
