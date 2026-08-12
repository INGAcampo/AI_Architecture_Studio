"""Servicio central de preferencias de AIAS."""
from __future__ import annotations

import json
from pathlib import Path


class SettingsManager:
    DEFAULTS = {
        "application": {
            "language": "es",
            "theme": "dark",
        },
        "paths": {
            "projects": "projects",
            "library": "biblioteca",
            "templates": "templates",
        },
        "autosave": {
            "enabled": True,
            "interval_seconds": 300,
        },
    }

    def __init__(self, config_file: str | Path = "config/settings.json"):
        self.config_file = Path(config_file)
        self.data = self._clone_defaults()
        self.load()

    def _clone_defaults(self):
        return json.loads(json.dumps(self.DEFAULTS))

    def load(self):
        if not self.config_file.exists():
            return self.data
        try:
            loaded = json.loads(self.config_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self.data
        self._merge(self.data, loaded)
        return self.data

    def save(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(
            json.dumps(self.data, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def get(self, dotted_key: str, default=None):
        value = self.data
        for part in dotted_key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, dotted_key: str, value):
        parts = dotted_key.split(".")
        target = self.data
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = value
        return value

    @classmethod
    def _merge(cls, target, source):
        for key, value in source.items():
            if isinstance(value, dict) and isinstance(target.get(key), dict):
                cls._merge(target[key], value)
            else:
                target[key] = value
