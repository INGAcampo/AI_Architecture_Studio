from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class SyncItem:
    bim_id:str
    structural_id:str
    revision:int

@dataclass(frozen=True,slots=True)
class SyncReport:
    created:tuple[str,...]
    updated:tuple[str,...]
    unchanged:tuple[str,...]

class BimStructuralSynchronization:
    def synchronize(self,bim_objects,structural_objects,links):
        created=[];updated=[];unchanged=[]
        structural_revisions={k:v for k,v in structural_objects.items()}
        for bim_id,bim_revision in bim_objects.items():
            link=links.get(bim_id)
            if link is None:
                created.append(bim_id)
            elif structural_revisions.get(link,-1)!=bim_revision:
                updated.append(bim_id)
            else:
                unchanged.append(bim_id)
        return SyncReport(tuple(sorted(created)),tuple(sorted(updated)),tuple(sorted(unchanged)))
