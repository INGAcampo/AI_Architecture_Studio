from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from aias_i18n import tr

class InspectorFilter(str, Enum):
    ALL='all'; EDITABLE='editable'; SHARED='shared'; CALCULATED='calculated'; IFC='ifc'; MODIFIED='modified'

@dataclass
class InspectorProperty:
    name:str; display_name:str; value:Any; group:str='General'; property_type:str='text'; unit:str|None=None
    editable:bool=True; visible:bool=True; shared:bool=False; calculated:bool=False; ifc:bool=False; modified:bool=False
    setter:Callable[[Any],None]|None=None
    def matches(self,text:str)->bool:
        q=str(text).strip().casefold()
        if not q:return True
        return q in ' '.join((self.name,self.display_name,self.group,str(self.value),self.unit or '')).casefold()
    def set_value(self,value:Any)->None:
        if not self.editable: raise PermissionError(tr("inspector.read_only",name=self.display_name))
        if self.setter is None: raise RuntimeError(tr("inspector.no_editor",name=self.display_name))
        self.setter(value); self.value=value; self.modified=True

class InspectorController:
    def __init__(self,property_service=None,shared_library=None):
        self.property_service=property_service; self.shared_library=shared_library; self.clear()
    @property
    def properties(self): return tuple(self._properties)
    def clear(self): self.element=None; self.owner_id=None; self._properties=[]
    def inspect(self,element):
        self.clear()
        if element is None:return ()
        self.element=element; self.owner_id=self._owner_id(element)
        merged={}
        for item in (*self._native(element),*self._service()): merged[item.name.casefold()]=item
        self._properties=sorted(merged.values(),key=lambda x:(self._order(x.group),x.display_name.casefold()))
        return self.properties
    def query(self,search='',active_filter=InspectorFilter.ALL):
        f=InspectorFilter(active_filter); out=[]
        for p in self._properties:
            if not p.visible or not p.matches(search):continue
            if f is InspectorFilter.EDITABLE and not p.editable:continue
            if f is InspectorFilter.SHARED and not p.shared:continue
            if f is InspectorFilter.CALCULATED and not p.calculated:continue
            if f is InspectorFilter.IFC and not p.ifc:continue
            if f is InspectorFilter.MODIFIED and not p.modified:continue
            out.append(p)
        return tuple(out)
    def grouped(self,search='',active_filter=InspectorFilter.ALL):
        groups={}
        for p in self.query(search,active_filter):groups.setdefault(p.group,[]).append(p)
        return {k:tuple(v) for k,v in groups.items()}
    def update(self,name,value):
        key=str(name).strip().casefold()
        for p in self._properties:
            if p.name.casefold()==key:p.set_value(value);return p
        raise KeyError(name)
    def _service(self):
        s=self.property_service
        if s is None or self.owner_id is None:return ()
        try: values=s.properties_for(self.owner_id)
        except Exception:return ()
        out=[]
        for pv in values:
            d=pv.definition; name=d.name; group=str(getattr(d.group,'value',d.group))
            def setter(value,s=s,owner=self.owner_id,name=name):s.set_value(owner,name,value)
            out.append(InspectorProperty(name,d.display_name,pv.value,group,d.property_type.value,d.unit,not d.read_only,d.visible,pv.source=='shared',pv.calculated,self._has_ifc(name),False,setter))
        return tuple(out)
    def _native(self,e):
        data={}
        info=getattr(e,'info',None)
        if callable(info):
            try:
                raw=info()
                if isinstance(raw,dict):data.update(raw)
            except Exception:pass
        nested=data.pop('Propiedades',None)
        if isinstance(nested,dict):
            for k,v in nested.items():data.setdefault(str(k),v)
        props=getattr(e,'properties',None)
        if isinstance(props,dict):
            for k,v in props.items():data.setdefault(str(k),v)
        for a,label in [('name','Nombre'),('type','Tipo'),('category','Categoría'),('level','Nivel'),('family','Familia')]:
            if hasattr(e,a):data.setdefault(label,getattr(e,a))
        return tuple(InspectorProperty(str(k),str(k),v,self._group(str(k)),self._type(v),editable=(self._setter(e,str(k)) is not None),setter=self._setter(e,str(k))) for k,v in data.items())
    @staticmethod
    def _owner_id(e):
        for a in ('id','element_id','guid','uuid','name'):
            v=getattr(e,a,None)
            if v is not None:return str(v)
        return str(id(e))
    @staticmethod
    def _setter(e,name):
        props=getattr(e,'properties',None)
        if isinstance(props,dict) and name in props:return lambda value:props.__setitem__(name,value)
        aliases={'Nombre':'name','Tipo':'type','Categoría':'category','Nivel':'level','Familia':'family'}
        for a in (name,name.lower().replace(' ','_'),aliases.get(name,'')):
            if a and hasattr(e,a):return lambda value,a=a:setattr(e,a,value)
        return None
    def _has_ifc(self,name):
        try:p=self.shared_library.get(name) if self.shared_library else None
        except Exception:p=None
        return bool(p and getattr(p,'ifc_mapping',None))
    @staticmethod
    def _type(v):
        if isinstance(v,bool):return 'boolean'
        if isinstance(v,int):return 'integer'
        if isinstance(v,float):return 'decimal'
        return 'text'
    @staticmethod
    def _group(name):
        n=name.casefold()
        for g,t in [('Geometry',('height','width','length','thickness','area','volume','altura','ancho','longitud','espesor','área','volumen')),('Materials',('material','finish','acabado')),('Structural',('strength','concrete','steel','load','resistencia','concreto','acero','carga')),('Cost',('cost','price','costo','precio')),('Identity',('name','type','category','family','nombre','tipo','categoría','familia','manufacturer','model')),('Constraints',('level','constraint','nivel','restricción'))]:
            if any(x in n for x in t):return g
        return 'Custom'
    @staticmethod
    def _order(g):return {'Identity':0,'Geometry':1,'Constraints':2,'Materials':3,'Structural':4,'Analysis':5,'Loads':6,'MEP':7,'Energy':8,'Cost':9,'Custom':12,'General':13}.get(str(g),99)
