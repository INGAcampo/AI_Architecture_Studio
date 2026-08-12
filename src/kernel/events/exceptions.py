"""Excepciones del framework de eventos AIAS."""


class EventFrameworkError(Exception):
    """Error base del framework."""


class EventDispatchError(EventFrameworkError):
    """Uno o más consumidores fallaron durante una publicación estricta."""

    def __init__(self, event_name: str, errors: list[BaseException]) -> None:
        self.event_name = event_name
        self.errors = tuple(errors)
        super().__init__(
            f"El evento {event_name!r} produjo {len(errors)} error(es) de consumidor."
        )
