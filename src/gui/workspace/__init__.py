from .events import WorkspaceEvent, WorkspaceEventSink
from .layout import LayoutManager, WorkspaceSerializer
from .manager import WorkspaceManager
from .model import (
    DockArea,
    DocumentSession,
    PanelDescriptor,
    PanelState,
    WorkspaceState,
)
from .panels import DockManager, PanelManager, PanelRegistry
from .qt_docking import (
    DockWidgetFactory,
    DockWidgetRecord,
    QtDockingController,
    QtUnavailableError,
    dock_area_to_qt,
    qt_area_to_dock_area,
    require_qt,
)
from .window_layout import WindowLayoutCoordinator, WindowLayoutSnapshot

__all__ = [
    "DockArea",
    "DockManager",
    "DockWidgetFactory",
    "DockWidgetRecord",
    "DocumentSession",
    "LayoutManager",
    "PanelDescriptor",
    "PanelManager",
    "PanelRegistry",
    "PanelState",
    "QtDockingController",
    "QtUnavailableError",
    "WindowLayoutCoordinator",
    "WindowLayoutSnapshot",
    "WorkspaceEvent",
    "WorkspaceEventSink",
    "WorkspaceManager",
    "WorkspaceSerializer",
    "WorkspaceState",
    "dock_area_to_qt",
    "qt_area_to_dock_area",
    "require_qt",
]

# --- AIAS WORKSPACE LEGACY COMPATIBILITY BRIDGE BEGIN ---
# Compatibility bridge for the historical src/gui/workspace.py module.
# Python resolves gui.workspace to this package because the package and module
# share the same import name. Load the historical module under a private gui
# module name so its package-relative imports retain gui semantics.
from importlib.util import module_from_spec as _module_from_spec
from importlib.util import spec_from_file_location as _spec_from_file_location
from pathlib import Path as _Path
import sys as _sys

_legacy_workspace_name = "gui._aias_legacy_workspace"
_legacy_workspace_path = _Path(__file__).resolve().parent.parent / "workspace.py"

if _legacy_workspace_name in _sys.modules:
    _legacy_workspace_module = _sys.modules[_legacy_workspace_name]
else:
    _legacy_workspace_spec = _spec_from_file_location(
        _legacy_workspace_name,
        _legacy_workspace_path,
    )
    if _legacy_workspace_spec is None or _legacy_workspace_spec.loader is None:
        raise ImportError(
            f"workspace_compat_import_error:{_legacy_workspace_path}"
        )
    _legacy_workspace_module = _module_from_spec(_legacy_workspace_spec)
    _sys.modules[_legacy_workspace_name] = _legacy_workspace_module
    _legacy_workspace_spec.loader.exec_module(_legacy_workspace_module)

Workspace = _legacy_workspace_module.Workspace

try:
    __all__
except NameError:
    __all__ = []
if "Workspace" not in __all__:
    __all__.append("Workspace")
# --- AIAS WORKSPACE LEGACY COMPATIBILITY BRIDGE END ---
