"""Executable demonstration of the Level 2 BIM vertical slice."""
from pathlib import Path
from tempfile import TemporaryDirectory
from .service import VerticalSliceService

def main():
    service=VerticalSliceService()
    walls=[
        service.create_wall((0,0),(8,0)),
        service.create_wall((8,0),(8,6)),
        service.create_wall((8,6),(0,6)),
        service.create_wall((0,6),(0,0)),
    ]
    door=service.add_opening("door",walls[0].id,1.0,0.9,2.1)
    window=service.add_opening("window",walls[1].id,2.0,1.5,1.2,0.9)
    room=service.create_room([w.id for w in walls],"Room 101")
    service.set_property(walls[0].id,"level","Level 1")
    service.select(walls[0].id,door.id,window.id,room.id)
    with TemporaryDirectory() as folder:
        path=service.save(Path(folder)/"vertical_slice.aias.json")
        loaded=VerticalSliceService.load(path)
        print(loaded.workspace_projection())

if __name__=="__main__":main()
