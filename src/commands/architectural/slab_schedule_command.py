"""SLABSCHEDULE 5.0.8.4 — cuadro estructural de losas."""

from commands.base_command import BaseCommand
from engines.architectural.slab_engine import SlabEngine


class SlabScheduleCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "SLABSCHEDULE"

    def begin(self, canvas):
        scene = getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )
        SlabEngine.update_scene_slabs(scene)

        slabs = [
            slab
            for slab in SlabEngine.scene_slabs(scene)
            if getattr(slab, "valid", False)
        ]

        print("SLAB STRUCTURAL SCHEDULE 5.0.8.4")
        print("-" * 152)
        print(
            f"{'Ambiente':<20}"
            f"{'Material':<24}"
            f"{'e(m)':>7}"
            f"{'f c MPa':>9}"
            f"{'Área':>10}"
            f"{'Vol.':>10}"
            f"{'PP kg/m²':>11}"
            f"{'CM kg/m²':>11}"
            f"{'CV kg/m²':>11}"
            f"{'Servicio':>12}"
            f"{'Carga total kg':>16}"
        )
        print("-" * 152)

        total_area = 0.0
        total_volume = 0.0
        total_service_kg = 0.0

        for slab in slabs:
            room_name = getattr(
                getattr(slab, "host_room", None),
                "name",
                "-",
            )
            print(
                f"{room_name[:18]:<20}"
                f"{slab.material[:22]:<24}"
                f"{slab.thickness:>7.3f}"
                f"{slab.concrete_strength_mpa:>9.1f}"
                f"{slab.area:>10.2f}"
                f"{slab.volume:>10.3f}"
                f"{slab.self_weight_kg_m2:>11.1f}"
                f"{slab.total_dead_load_kg_m2:>11.1f}"
                f"{slab.live_load_kg_m2:>11.1f}"
                f"{slab.total_service_load_kg_m2:>12.1f}"
                f"{slab.total_service_load_kg:>16.1f}"
            )

            total_area += slab.area
            total_volume += slab.volume
            total_service_kg += slab.total_service_load_kg

        print("-" * 152)
        print(f"Losas: {len(slabs)}")
        print(f"Área total: {total_area:.2f} m²")
        print(f"Volumen total: {total_volume:.3f} m³")
        print(
            f"Carga total de servicio: "
            f"{total_service_kg:.2f} kg"
        )

        window_getter = getattr(canvas, "window", None)
        window = window_getter() if callable(window_getter) else None
        if window is not None:
            window.statusBar().showMessage(
                f"SLABS: {len(slabs)} | "
                f"{total_area:.2f} m² | "
                f"{total_service_kg:.1f} kg"
            )

        manager = getattr(canvas, "tool_manager", None)
        cancel = getattr(manager, "cancel_current", None)
        if callable(cancel):
            cancel()
