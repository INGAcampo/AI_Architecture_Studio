from pathlib import Path
from models.project.project_document import ProjectDocument
from .loader import ProjectLoader
from .serializer import ProjectSerializer
class ProjectIO:
    def __init__(self): self.serializer=ProjectSerializer(); self.loader=ProjectLoader()
    def new_project(self,name='Sin título'): return ProjectDocument.create(name)
    def save(self,document,destination=None):
        target=Path(destination) if destination else document.file_path
        if target is None: raise ValueError('Debe indicar una ruta para guardar el proyecto')
        return self.serializer.serialize(document,target)
    def open(self,source): return self.loader.load(source)
