"""ROOMSCHEDULE 5.0.7.4 — cuadro de áreas en consola."""

from commands.base_command import BaseCommand
from engines.architectural.room_schedule import RoomSchedule


class RoomScheduleCommand(BaseCommand):
    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "ROOMSCHEDULE"

    def begin(self, canvas):
        scene = getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )
        report = RoomSchedule.console_report(scene)
        print(report)

        totals = RoomSchedule.totals(scene)
        window_getter = getattr(canvas, "window", None)
        window = window_getter() if callable(window_getter) else None
        if window is not None:
            window.statusBar().showMessage(
                f"ROOMS: {totals['count']} | "
                f"Área útil: {totals['area']:.2f} m²"
            )

        manager = getattr(canvas, "tool_manager", None)
        cancel = getattr(manager, "cancel_current", None)
        if callable(cancel):
            cancel()
