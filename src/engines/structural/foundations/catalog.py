class FoundationMaterialCatalog:
    def __init__(self): self._items = {}; self.revision = 0
    def register(self, item, replace=False):
        if item.material_id in self._items and not replace: raise KeyError(item.material_id)
        self._items[item.material_id] = item; self.revision += 1
    def get(self, material_id):
        try: return self._items[material_id]
        except KeyError as exc: raise KeyError(f"Material desconocido: {material_id}") from exc
    def remove(self, material_id):
        item = self.get(material_id); self._items.pop(material_id); self.revision += 1; return item
