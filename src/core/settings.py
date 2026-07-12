"""
AI Architecture Studio
Core Settings

Versión: Alpha 0.0.1
"""

from pathlib import Path
import json


class Settings:

    def __init__(self):

        self.config_folder = Path("config")
        self.config_folder.mkdir(exist_ok=True)

        self.config_file = self.config_folder / "settings.json"

        self.data = {
            "application": {
                "name": "AI Architecture Studio",
                "version": "0.0.1 Alpha",
                "language": "es",
                "theme": "dark"
            },

            "paths": {
                "projects": "projects",
                "library": "biblioteca",
                "templates": "templates"
            },

            "modules": {
                "architecture": True,
                "structure": False,
                "bim": False,
                "ai": False
            }
        }

    def save(self):

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def load(self):

        if self.config_file.exists():

            with open(self.config_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)

        else:

            self.save()


settings = Settings()
settings.load()