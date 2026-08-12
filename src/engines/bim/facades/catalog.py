class FacadePanelCatalog:
    def __init__(self):self._items={};self.revision=0
    def register(self,item,replace=False):
        if item.type_id in self._items and not replace:raise KeyError(item.type_id)
        self._items[item.type_id]=item;self.revision+=1
    def get(self,type_id):
        try:return self._items[type_id]
        except KeyError as exc:raise KeyError(f"Panel desconocido: {type_id}") from exc
    def remove(self,type_id):
        item=self.get(type_id);self._items.pop(type_id);self.revision+=1;return item
