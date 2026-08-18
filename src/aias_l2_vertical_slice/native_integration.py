"""Bridge the validated Level 2 vertical slice to native AIAS BIM/runtime services."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from aias_engineering_object.properties import PropertySystem
from aias_omega_core.graph import Relationship as OmegaRelationship
from aias_omega_core.ids import ObjectId
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.persistence import ProjectSerializer
from aias_omega_core.project import EngineeringProject
from aias_omega_core.selection import SelectionService
from bim_authoring.doors.engine import NativeBimDoorEngine
from bim_authoring.doors.model import (
    DoorFamily,
    DoorFrame,
    DoorHanding,
    DoorInstance,
    DoorOperation,
    DoorPanel,
    DoorType,
)
from bim_authoring.rooms_spaces import NativeBimRoomSpaceEngine, Room as NativeRoom
from bim_authoring.walls.engine import NativeBimWallEngine
from bim_authoring.walls.model import (
    CompoundStructure,
    WallInstance,
    WallLayer,
    WallLocationLine,
    WallProfile,
    WallType,
)
from bim_authoring.windows.engine import NativeBimWindowEngine
from bim_authoring.windows.model import (
    WindowFamily,
    WindowFrame,
    WindowGlass,
    WindowInstance,
    WindowOperation,
    WindowType,
)
from cad_professional_kernel.history import HistoryManager
from engines.ai.relationships.manager import RelationshipManager
from engines.ai.relationships.model import RelationshipDirection, RelationshipType
from engines.ai.relationships.propagation import PropagationEvent, RelationshipPropagationEngine
from gui.bim_workspace.builder import BimWorkspaceBuilder
from gui.bim_workspace.controller import BimWorkspaceController

from .model import BimProjectState, Opening, Room, Wall
from .service import VerticalSliceService


class NativeIntegrationError(RuntimeError):
    """Raised when canonical state cannot be represented by a selected native service."""


@dataclass(frozen=True, slots=True)
class NativeSyncReport:
    """Summarize one canonical-to-native synchronization pass."""

    walls: int
    doors: int
    windows: int
    rooms: int
    relationships: int
    workspace_nodes: int
    selected_objects: int


class _StateAction:
    def __init__(self, service: VerticalSliceService, before: BimProjectState, after: BimProjectState) -> None:
        self.service = service
        self.before = before
        self.after = after

    def do(self) -> None:
        self.service.state = self.after.clone()

    def undo(self) -> None:
        self.service.state = self.before.clone()


class NativeVerticalSliceBridge:
    """Coordinate the canonical vertical slice with native BIM, runtime and Workspace 2 services."""

    def __init__(self, service: VerticalSliceService) -> None:
        self.service = service
        self.properties = PropertySystem()
        self.history = HistoryManager()
        self.serializer = ProjectSerializer()
        self._canonical_to_native_id: dict[str, ObjectId] = {}
        self._native_to_canonical_id: dict[ObjectId, str] = {}
        self.wall_engine = NativeBimWallEngine()
        self.door_engine = NativeBimDoorEngine(self.wall_engine)
        self.window_engine = NativeBimWindowEngine(self.wall_engine)
        self.room_engine = NativeBimRoomSpaceEngine()
        self.relationships = RelationshipManager()
        self.propagation = RelationshipPropagationEngine(self.relationships.graph)
        self.selection = SelectionService()
        self.workspace_controller: BimWorkspaceController | None = None
        self.native_rooms: dict[str, NativeRoom] = {}
        self.project: EngineeringProject | None = None

    def synchronize(self) -> NativeSyncReport:
        """Rebuild all native mirrors from the current canonical project state."""
        self.wall_engine = NativeBimWallEngine()
        self.door_engine = NativeBimDoorEngine(self.wall_engine)
        self.window_engine = NativeBimWindowEngine(self.wall_engine)
        self.room_engine = NativeBimRoomSpaceEngine()
        self.relationships = RelationshipManager()
        self.propagation = RelationshipPropagationEngine(self.relationships.graph)
        self.native_rooms = {}

        for wall in self.service.state.walls.values():
            self.wall_engine.add_wall(self._native_wall(wall))
        for opening in self.service.state.openings.values():
            if opening.kind == "door":
                self._add_native_door(opening)
            elif opening.kind == "window":
                self._add_native_window(opening)
            else:
                raise NativeIntegrationError(f"unsupported_opening_kind:{opening.kind}")
        for room in self.service.state.rooms.values():
            self.native_rooms[room.id] = self._native_room(room)
        self._synchronize_relationships()
        self.project = self.build_engineering_project()
        self._synchronize_selection()
        self.workspace_controller = self.build_workspace_controller()
        return NativeSyncReport(
            walls=len(self.wall_engine.walls),
            doors=len(self.door_engine.doors),
            windows=len(self.window_engine.windows),
            rooms=len(self.native_rooms),
            relationships=len(self.relationships.graph),
            workspace_nodes=len(self.workspace_controller.tree.snapshot()["nodes"]),
            selected_objects=len(self.selection.all()),
        )

    def transact(self, mutation: Callable[[VerticalSliceService], Any]) -> Any:
        """Execute a canonical mutation under the native CAD history manager and resynchronize mirrors."""
        before = self.service.state.clone()
        try:
            result = mutation(self.service)
            after = self.service.state.clone()
        except Exception:
            self.service.state = before
            raise
        self.service.state = before
        undo_stack = getattr(self.service, "_undo", None)
        redo_stack = getattr(self.service, "_redo", None)
        if isinstance(undo_stack, list):
            undo_stack.clear()
        if isinstance(redo_stack, list):
            redo_stack.clear()
        self.history.execute(_StateAction(self.service, before, after))
        self.synchronize()
        return result

    def undo(self) -> bool:
        """Undo the last bridge transaction using the native CAD history manager."""
        changed = self.history.undo()
        if changed:
            self.synchronize()
        return changed

    def redo(self) -> bool:
        """Redo the last bridge transaction using the native CAD history manager."""
        changed = self.history.redo()
        if changed:
            self.synchronize()
        return changed

    def propagation_report(self, source_id: str, event_type: str = "property_changed"):
        """Return the native smart-relationship propagation report for a canonical object."""
        return self.propagation.propagate(PropagationEvent(source_id, event_type, {}))

    def build_engineering_project(self, name: str = "AIAS Level 2 Vertical Slice") -> EngineeringProject:
        """Project canonical objects and relationships into the native Omega engineering project model."""
        project = EngineeringProject(name)
        self._canonical_to_native_id = {}
        self._native_to_canonical_id = {}

        for canonical_id, obj in self._iter_canonical_objects():
            native = self._engineering_object(canonical_id, obj)
            project.add_object(native)
            self._canonical_to_native_id[canonical_id] = native.object_id
            self._native_to_canonical_id[native.object_id] = canonical_id

        marker = EngineeringObject(
            object_type="_aias_vertical_slice_state",
            name="AIAS Vertical Slice State",
            properties={
                "schema_version": self.service.state.schema_version,
                "revision": self.service.state.revision,
                "selection": list(self.service.state.selection),
                "relationships": [dict(item) for item in self.service.state.relationships],
            },
            metadata={"role": "vertical_slice_state"},
        )
        project.add_object(marker)

        for rel in self.service.state.relationships:
            source = self._canonical_to_native_id.get(rel["source"])
            target = self._canonical_to_native_id.get(rel["target"])
            if source is not None and target is not None:
                project.graph.add(OmegaRelationship(source, target, rel["type"]))
        return project

    def save_native(self, path: Path) -> Path:
        """Persist the synchronized project through the native Omega serializer."""
        project = self.build_engineering_project()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.serializer.save(project, path)
        self.project = project
        return path

    def load_native(self, path: Path) -> VerticalSliceService:
        """Load an Omega project and reconstruct an equivalent canonical vertical-slice service."""
        project = self.serializer.load(Path(path))
        state = BimProjectState()
        native_to_canonical: dict[ObjectId, str] = {}
        marker: EngineeringObject | None = None

        for obj in project.objects.values():
            if obj.metadata.get("role") == "vertical_slice_state":
                marker = obj
                continue
            canonical_id = str(obj.metadata.get("canonical_id", ""))
            if not canonical_id:
                continue
            native_to_canonical[obj.object_id] = canonical_id
            if obj.object_type == "wall":
                state.walls[canonical_id] = Wall(
                    id=canonical_id,
                    start=tuple(obj.geometry["start"]),
                    end=tuple(obj.geometry["end"]),
                    height=obj.geometry["height"],
                    thickness=obj.geometry["thickness"],
                    properties=dict(obj.properties),
                )
            elif obj.object_type in {"door", "window"}:
                state.openings[canonical_id] = Opening(
                    id=canonical_id,
                    kind=obj.object_type,
                    host_wall_id=str(obj.geometry["host_wall_id"]),
                    offset=obj.geometry["offset"],
                    width=obj.geometry["width"],
                    height=obj.geometry["height"],
                    sill_height=obj.geometry["sill_height"],
                    properties=dict(obj.properties),
                )
            elif obj.object_type == "room":
                state.rooms[canonical_id] = Room(
                    id=canonical_id,
                    boundary_wall_ids=list(obj.geometry["boundary_wall_ids"]),
                    name=obj.name or "Room",
                    properties=dict(obj.properties),
                )

        if marker is not None and "relationships" in marker.properties:
            state.relationships = [dict(item) for item in marker.properties.get("relationships", [])]
        else:
            state.relationships = [
                {
                    "type": rel.relation_type,
                    "source": native_to_canonical[rel.source],
                    "target": native_to_canonical[rel.target],
                }
                for rel in project.graph.all()
                if rel.source in native_to_canonical and rel.target in native_to_canonical
            ]
        if marker is not None:
            state.schema_version = str(marker.properties.get("schema_version", state.schema_version))
            state.revision = int(marker.properties.get("revision", 0))
            state.selection = [str(item) for item in marker.properties.get("selection", [])]
        restored = VerticalSliceService(state)
        self.service = restored
        self.project = project
        self.synchronize()
        return restored

    def build_workspace_controller(self) -> BimWorkspaceController:
        """Build a real Workspace 2 tree and controller from canonical BIM objects."""
        records = []
        for canonical_id, obj in self._iter_canonical_objects():
            if isinstance(obj, Wall):
                category = "Walls"
                name = obj.properties.get("name", canonical_id)
                level = obj.properties.get("level", "Nivel 0")
            elif isinstance(obj, Opening):
                category = "Doors" if obj.kind == "door" else "Windows"
                name = obj.properties.get("name", canonical_id)
                level = obj.properties.get("level", "Nivel 0")
            else:
                category = "Rooms"
                name = obj.name
                level = obj.properties.get("level", "Nivel 0")
            records.append({
                "object_id": canonical_id,
                "name": str(name),
                "object_type": category,
                "category": category,
                "level_name": str(level),
                "phase": str(obj.properties.get("phase", "New Construction")),
            })
        tree = BimWorkspaceBuilder().build(records, title="AIAS BIM Workspace")
        controller = BimWorkspaceController(tree)
        if self.service.state.selection:
            controller.select_object(self.service.state.selection[0])
        return controller

    def workspace_snapshot(self) -> dict[str, Any]:
        """Return the native Workspace 2 tree and UI-state snapshot."""
        controller = self.build_workspace_controller()
        return {"tree": controller.tree.snapshot(), "state": controller.state.snapshot()}

    def _native_wall(self, wall: Wall) -> WallInstance:
        material = str(wall.properties.get("material_id", "MAT-GENERIC"))
        layer = WallLayer(f"LAYER-{wall.id}", material, float(wall.thickness), "core")
        wall_type = WallType(
            f"TYPE-{wall.id}",
            str(wall.properties.get("type_name", "AIAS Basic Wall")),
            CompoundStructure((layer,)),
        )
        profile = WallProfile(
            (float(wall.start[0]), float(wall.start[1]), 0.0),
            (float(wall.end[0]), float(wall.end[1]), 0.0),
            float(wall.properties.get("base_elevation", 0.0)),
            float(wall.height),
        )
        return WallInstance(
            wall.id,
            wall_type,
            profile,
            WallLocationLine.CENTERLINE,
            str(wall.properties.get("level", "LEVEL-0")),
            dict(wall.properties),
        )

    def _add_native_door(self, opening: Opening) -> None:
        panel = DoorPanel(f"PANEL-{opening.id}", "MAT-DOOR", 0.04)
        frame = DoorFrame(f"FRAME-{opening.id}", "MAT-FRAME", 0.12, 0.08)
        door_type = DoorType(
            f"TYPE-{opening.id}", "AIAS Door", float(opening.width), float(opening.height),
            DoorOperation.SINGLE_SWING, DoorHanding.LEFT, panel, frame,
        )
        family = DoorFamily(f"FAMILY-{opening.id}", "AIAS Door Family", (door_type,))
        self.door_engine.register_family(family)
        self.door_engine.add_door(DoorInstance(
            opening.id, family.family_id, door_type, opening.host_wall_id,
            float(opening.offset), float(opening.sill_height),
            level_id=str(opening.properties.get("level", "LEVEL-0")),
            properties=dict(opening.properties),
        ))

    def _add_native_window(self, opening: Opening) -> None:
        frame = WindowFrame(f"FRAME-{opening.id}", "MAT-FRAME", 0.12, 0.05)
        glass = WindowGlass(f"GLASS-{opening.id}", "MAT-GLASS", 0.006, 2.8, 0.55)
        window_type = WindowType(
            f"TYPE-{opening.id}", "AIAS Window", float(opening.width), float(opening.height),
            WindowOperation.FIXED, frame, glass,
        )
        family = WindowFamily(f"FAMILY-{opening.id}", "AIAS Window Family", (window_type,))
        self.window_engine.register_family(family)
        self.window_engine.add_window(WindowInstance(
            opening.id, family.family_id, window_type, opening.host_wall_id,
            float(opening.offset), float(opening.sill_height),
            level_id=str(opening.properties.get("level", "LEVEL-0")),
            properties=dict(opening.properties),
        ))

    def _native_room(self, room: Room) -> NativeRoom:
        points: list[tuple[float, float]] = []
        for wall_id in room.boundary_wall_ids:
            wall = self.service.state.walls[wall_id]
            point = (float(wall.start[0]), float(wall.start[1]))
            if point not in points:
                points.append(point)
        if len(points) < 3:
            raise NativeIntegrationError(f"room_boundary_not_resolvable:{room.id}")
        return NativeRoom(
            room.id,
            room.name,
            tuple(points),
            float(room.properties.get("height", 3.0)),
            str(room.properties.get("level", "LEVEL-0")),
        )

    def _synchronize_relationships(self) -> None:
        for index, rel in enumerate(self.service.state.relationships):
            rel_type = RelationshipType.HOSTS if rel["type"] == "HOSTS" else RelationshipType.CUSTOM
            self.relationships.connect(
                f"VS-{index:06d}", rel["source"], rel["target"], rel_type,
                RelationshipDirection.DIRECTED,
                metadata={"canonical_type": rel["type"]},
            )

    def _synchronize_selection(self) -> None:
        self.selection = SelectionService()
        selected = [
            self._canonical_to_native_id[item]
            for item in self.service.state.selection
            if item in self._canonical_to_native_id
        ]
        self.selection.set(selected)

    def _engineering_object(self, canonical_id: str, obj: Wall | Opening | Room) -> EngineeringObject:
        if isinstance(obj, Wall):
            object_type = "wall"
            geometry = {
                "start": list(obj.start), "end": list(obj.end),
                "height": obj.height, "thickness": obj.thickness,
            }
            name = str(obj.properties.get("name", canonical_id))
        elif isinstance(obj, Opening):
            object_type = obj.kind
            geometry = {
                "host_wall_id": obj.host_wall_id, "offset": obj.offset,
                "width": obj.width, "height": obj.height, "sill_height": obj.sill_height,
            }
            name = str(obj.properties.get("name", canonical_id))
        else:
            object_type = "room"
            geometry = {"boundary_wall_ids": list(obj.boundary_wall_ids)}
            name = obj.name
        return EngineeringObject(
            object_type=object_type,
            name=name,
            geometry=geometry,
            properties=dict(obj.properties),
            classification=f"AIAS::{object_type.upper()}",
            metadata={"canonical_id": canonical_id, "vertical_slice": True},
        )

    def _iter_canonical_objects(self):
        yield from self.service.state.walls.items()
        yield from self.service.state.openings.items()
        yield from self.service.state.rooms.items()
