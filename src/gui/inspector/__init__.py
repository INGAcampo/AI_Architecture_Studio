from .controller import InspectorController, InspectorFilter, InspectorProperty
try:
    from .panel import BimPropertyInspector
except ImportError:
    BimPropertyInspector = None

__all__ = ["BimPropertyInspector", "InspectorController", "InspectorFilter", "InspectorProperty"]
