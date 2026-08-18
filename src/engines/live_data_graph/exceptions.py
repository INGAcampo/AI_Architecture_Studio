"""Excepciones del AIAS Live Data Graph."""


class LiveDataGraphError(Exception):
    """Error base del motor."""


class DuplicateNodeError(LiveDataGraphError):
    """Se intentó registrar un nodo existente."""


class NodeNotFoundError(LiveDataGraphError, KeyError):
    """No existe el nodo solicitado."""


class DependencyCycleError(LiveDataGraphError):
    """La dependencia solicitada produciría un ciclo."""
