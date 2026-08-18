from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class LibraryItem:
    item_id:str;category:str;version:int;payload:dict
class FamilyLibraryManager:
    def __init__(self): self._items={}
    def add(self,item):
        current=self._items.get(item.item_id)
        if current and current.version>=item.version: raise ValueError("Versión no válida")
        self._items[item.item_id]=item
    def get(self,item_id): return self._items[item_id]
    def by_category(self,category): return tuple(sorted((i for i in self._items.values() if i.category==category),key=lambda x:x.item_id))
    def export_index(self): return {k:{"category":v.category,"version":v.version} for k,v in sorted(self._items.items())}
