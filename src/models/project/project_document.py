from dataclasses import dataclass,field
from pathlib import Path
from .metadata import ProjectMetadata
from .settings import ProjectSettings
@dataclass
class ProjectDocument:
    metadata:ProjectMetadata=field(default_factory=ProjectMetadata)
    settings:ProjectSettings=field(default_factory=ProjectSettings)
    objects:list=field(default_factory=list); layers:list=field(default_factory=list)
    camera:dict=field(default_factory=dict); custom_data:dict=field(default_factory=dict)
    file_path:Path|None=None; dirty:bool=False
    @classmethod
    def create(cls,name="Sin título"):
        return cls(metadata=ProjectMetadata(name=name),layers=[{"name":"0","visible":True,"locked":False,"color":"#FFFFFF","lineweight":0.25}],camera={"center":[0.0,0.0,0.0],"zoom":1.0,"rotation":0.0})
    def mark_dirty(self): self.dirty=True; self.metadata.touch()
    def mark_clean(self): self.dirty=False
    def add_object(self,data): self.objects.append(data); self.mark_dirty()
    def remove_object(self,object_id):
        for i,item in enumerate(self.objects):
            if item.get("id")==object_id: del self.objects[i]; self.mark_dirty(); return True
        return False
    def set_custom_data(self,key,value): self.custom_data[key]=value; self.mark_dirty()
    def save(self,destination=None):
        from storage.project_io import ProjectIO
        return ProjectIO().save(self,destination)
    @classmethod
    def load(cls,source):
        from storage.project_io import ProjectIO
        return ProjectIO().open(source)
