"""End-to-end BIM vertical-slice application service."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .model import BimProjectState,Wall,Opening,Room

class VerticalSliceError(ValueError):
    """Raised when a vertical-slice invariant is violated."""

class VerticalSliceService:
    """Coordinate creation, relationships, history, persistence and workspace projection."""

    def __init__(self,state:BimProjectState|None=None):
        self.state=state or BimProjectState()
        self._undo:list[BimProjectState]=[]
        self._redo:list[BimProjectState]=[]

    def _checkpoint(self)->None:
        self._undo.append(self.state.clone());self._redo.clear()

    def _changed(self)->None:
        self.state.revision+=1

    def create_wall(self,start:tuple[float,float],end:tuple[float,float],**kwargs)->Wall:
        if start==end:raise VerticalSliceError("wall_requires_nonzero_length")
        self._checkpoint();wall=Wall(start=start,end=end,**kwargs);self.state.walls[wall.id]=wall;self._changed();return wall

    def add_opening(self,kind:str,wall_id:str,offset:float,width:float,height:float,sill_height:float=0.0,**kwargs)->Opening:
        if kind not in {"door","window"}:raise VerticalSliceError("unsupported_opening_kind")
        wall=self.state.walls.get(wall_id)
        if wall is None:raise VerticalSliceError("unknown_host_wall")
        if width<=0 or height<=0:raise VerticalSliceError("invalid_opening_dimensions")
        if offset<0 or offset+width>wall.length():raise VerticalSliceError("opening_outside_wall")
        self._checkpoint()
        opening=Opening(kind=kind,host_wall_id=wall_id,offset=offset,width=width,height=height,sill_height=sill_height,**kwargs)
        self.state.openings[opening.id]=opening
        self.state.relationships.append({"type":"HOSTS","source":wall_id,"target":opening.id})
        self._changed();return opening

    def create_room(self,wall_ids:list[str],name:str="Room",**kwargs)->Room:
        if len(wall_ids)<3:raise VerticalSliceError("room_requires_three_walls")
        missing=[x for x in wall_ids if x not in self.state.walls]
        if missing:raise VerticalSliceError(f"unknown_room_walls:{missing}")
        self._checkpoint();room=Room(boundary_wall_ids=list(wall_ids),name=name,**kwargs);self.state.rooms[room.id]=room
        for wall_id in wall_ids:self.state.relationships.append({"type":"BOUNDS","source":wall_id,"target":room.id})
        self._changed();return room

    def set_property(self,object_id:str,key:str,value:Any)->None:
        obj=self._object(object_id);self._checkpoint();obj.properties[key]=value;self._propagate(object_id,key,value);self._changed()

    def _object(self,object_id:str):
        return self.state.walls.get(object_id) or self.state.openings.get(object_id) or self.state.rooms.get(object_id) or (_ for _ in ()).throw(VerticalSliceError("unknown_object"))

    def _propagate(self,source_id:str,key:str,value:Any)->None:
        if key!="level":return
        for rel in self.state.relationships:
            if rel["source"]==source_id and rel["type"]=="HOSTS":
                self.state.openings[rel["target"]].properties["level"]=value

    def select(self,*object_ids:str)->None:
        for object_id in object_ids:self._object(object_id)
        self.state.selection=list(dict.fromkeys(object_ids))

    def undo(self)->bool:
        if not self._undo:return False
        self._redo.append(self.state.clone());self.state=self._undo.pop();return True

    def redo(self)->bool:
        if not self._redo:return False
        self._undo.append(self.state.clone());self.state=self._redo.pop();return True

    def save(self,path:Path)->Path:
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(self.state.to_dict(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return path

    @classmethod
    def load(cls,path:Path)->"VerticalSliceService":
        data=json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(BimProjectState.from_dict(data))

    def workspace_projection(self)->dict[str,Any]:
        return {
            "revision":self.state.revision,
            "tree":[
                {"category":"Walls","objects":[self._row(x) for x in self.state.walls.values()]},
                {"category":"Openings","objects":[self._row(x) for x in self.state.openings.values()]},
                {"category":"Rooms","objects":[self._row(x) for x in self.state.rooms.values()]},
            ],
            "selection":list(self.state.selection),
        }

    @staticmethod
    def _row(obj)->dict[str,Any]:
        return {"id":obj.id,"type":type(obj).__name__,"properties":dict(obj.properties)}

