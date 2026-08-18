class AnalyticalModelManager:
    def __init__(self):self._items={};self._by_source={}
    def add(self,obj):
        if obj.object_id in self._items:raise KeyError(obj.object_id)
        self._items[obj.object_id]=obj;self._by_source.setdefault(obj.source_id,set()).add(obj.object_id);return obj
    def get(self,oid):return self._items[oid]
    def for_source(self,sid):return tuple(self._items[i] for i in sorted(self._by_source.get(sid,set())))
    def active(self):return tuple(o for o in self._items.values() if o.active)
    def snapshot(self):return tuple(sorted((o.object_id,o.kind.value,o.source_id,o.active) for o in self._items.values()))
