from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class RegenerationRecord:
    object_id:str
    previous_revision:int
    new_revision:int
    outputs:dict

class StructuralRegenerationEngine:
    def regenerate(self,obj,revision,builders):
        outputs={name:builder(obj) for name,builder in builders.items()}
        return RegenerationRecord(getattr(obj,"member_id",getattr(obj,"slab_id",getattr(obj,"foundation_id","unknown"))),max(0,revision-1),revision,outputs)
    def batch(self,items,builders):
        return tuple(self.regenerate(obj,revision,builders) for obj,revision in items)
