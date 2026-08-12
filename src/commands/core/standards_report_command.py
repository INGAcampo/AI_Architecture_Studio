"""Comando NORMASREPORT / STANDARDSREPORT."""

from commands.base_command import BaseCommand
from core.standards.standard_manager import StandardManager


class StandardsReportCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "STANDARDSREPORT"

    def begin(self, canvas):
        manager = StandardManager.instance()
        print(manager.report())

        window_getter = getattr(canvas, "window", None)
        window = window_getter() if callable(window_getter) else None
        if window is not None:
            profile = manager.active_profile
            window.statusBar().showMessage(
                f"NORMAS: {profile.name} | "
                f"{'Verificado' if profile.verified else 'Pendiente'}"
            )

        tool_manager = getattr(canvas, "tool_manager", None)
        cancel = getattr(tool_manager, "cancel_current", None)
        if callable(cancel):
            cancel()
