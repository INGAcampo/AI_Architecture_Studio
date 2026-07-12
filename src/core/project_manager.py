"""
AI Architecture Studio
Project Manager

Versión: Alpha 0.2
"""

import json
from pathlib import Path
from datetime import datetime

from core.logger import logger


class ProjectManager:

    def __init__(self):
        self.projects_folder = Path("projects")
        self.projects_folder.mkdir(exist_ok=True)

    def create_project(self, name, client="", location="", standard="ACI 318"):
        safe_name = name.replace(" ", "_")

        project_folder = self.projects_folder / safe_name
        project_folder.mkdir(exist_ok=True)

        project_data = {
            "project": {
                "name": name,
                "client": client,
                "location": location,
                "standard": standard,
                "created_at": datetime.now().isoformat(),
                "version": "0.1"
            },
            "disciplines": {
                "architecture": True,
                "structure": True,
                "bim": False,
                "cost": False,
                "ai": True
            }
        }

        project_file = project_folder / f"{safe_name}.aias.json"

        with open(project_file, "w", encoding="utf-8") as file:
            json.dump(project_data, file, indent=4, ensure_ascii=False)

        logger.info(f"Proyecto creado: {name}")

        return project_file