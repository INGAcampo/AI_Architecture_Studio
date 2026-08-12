class FiniteElementLibrary:
    def __init__(self): self._elements={}
    def register(self,element):
        if element.element_id in self._elements: raise ValueError("Elemento duplicado")
        self._elements[element.element_id]=element
        return element
    def get(self,element_id): return self._elements[element_id]
    def all(self): return tuple(self._elements[k] for k in sorted(self._elements))
    def by_type(self,type_name):
        return tuple(e for e in self.all() if type(e).__name__==type_name)
