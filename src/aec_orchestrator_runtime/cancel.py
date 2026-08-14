from __future__ import annotations


class CancellationToken:
    def __init__(self) -> None:
        self._cancelled=False
        self._reason=None

    def cancel(self, reason: str="cancelled") -> None:
        if not reason.strip():
            raise ValueError("cancellation reason must not be empty")
        if not self._cancelled:
            self._cancelled=True
            self._reason=reason

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    @property
    def reason(self):
        return self._reason
