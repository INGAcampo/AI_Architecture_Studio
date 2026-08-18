"""
AI Architecture Studio
FILLET Professional 4.1.1

Soporta:
- LINE ↔ LINE
- dos segmentos adyacentes de la misma PLINE
- LINE ↔ segmento PLINE
- segmento PLINE ↔ segmento PLINE
"""

from commands.base_command import BaseCommand
from core.history.fillet_action import FilletAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class FilletCommand(BaseCommand):

    PICK_TOLERANCE = 0.55

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "FILLET"
        self.radius = 1.0
        self.first_pick_record = None
        self.awaiting_radius = False

    def activate(self):
        super().activate()
        print(
            "FILLET activo: radio=1.0. "
            "Selecciona LINE o segmento de PLINE; escribe R"
        )

    def _canvas_point(self, canvas):
        getter = getattr(canvas, "get_input_point", None)

        if callable(getter):
            return getter()

        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    def _window(self, canvas):
        getter = getattr(canvas, "window", None)
        return getter() if callable(getter) else None

    def _prompt(self, canvas, text):
        window = self._window(canvas)
        command_line = getattr(window, "command_line", None)

        if command_line is not None:
            command_line.set_prompt(text)

    def _status(self, canvas, text):
        window = self._window(canvas)

        if window is not None:
            window.statusBar().showMessage(text)

    def _scene(self, canvas):
        return getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

    def _records(self, canvas, point):
        scene = self._scene(canvas)

        if scene is None:
            return []

        records = []

        for element in scene.get_elements():
            geometry = getattr(element, "geometry", None)

            if (
                geometry is not None
                and geometry.__class__.__name__ == "Line"
            ):
                distance = (
                    GeometryBuilder.distance_to_line_segment(
                        geometry,
                        point,
                    )
                )
                records.append(
                    {
                        "element": element,
                        "segment": geometry,
                        "index": None,
                        "distance": distance,
                        "pick": point,
                    }
                )
                continue

            if element.__class__.__name__ == "CadPolyline":
                for index, segment in (
                    GeometryBuilder.polyline_segment_records(
                        element
                    )
                ):
                    distance = (
                        GeometryBuilder.distance_to_line_segment(
                            segment,
                            point,
                        )
                    )
                    records.append(
                        {
                            "element": element,
                            "segment": segment,
                            "index": index,
                            "distance": distance,
                            "pick": point,
                        }
                    )

        return sorted(
            records,
            key=lambda item: item["distance"],
        )

    def _find_record(self, canvas, point):
        for record in self._records(canvas, point):
            if record["distance"] > self.PICK_TOLERANCE:
                break

            first = self.first_pick_record

            if first is None:
                return record

            same_segment = (
                record["element"] is first["element"]
                and record["index"] == first["index"]
            )

            if not same_segment:
                return record

        return None

    def mouse_move(self, event, canvas):
        point = self._canvas_point(canvas)
        record = self._find_record(canvas, point)

        canvas.highlight.clear()
        canvas.preview_geometry = None

        if record is not None:
            canvas.highlight.set(record["element"])

            if self.first_pick_record is not None:
                result = GeometryBuilder.create_fillet_from_lines(
                    self.first_pick_record["segment"],
                    record["segment"],
                    self.first_pick_record["pick"],
                    point,
                    self.radius,
                )

                if result is not None:
                    _, _, arc = result
                    canvas.preview_geometry = arc

        canvas.update()

    def mouse_press(self, event, canvas):
        point = self._canvas_point(canvas)
        record = self._find_record(canvas, point)

        if record is None:
            message = (
                "FILLET: no se encontró una LINE o "
                "segmento recto de PLINE cerca del cursor"
            )
            print(message)
            self._status(canvas, message)
            return

        record["pick"] = point

        if self.first_pick_record is None:
            self.first_pick_record = record
            print("FILLET: primer segmento seleccionado")
            self._prompt(canvas, "Seleccione segundo segmento:")
            return

        first = self.first_pick_record

        if (
            first["element"] is record["element"]
            and first["element"].__class__.__name__ == "CadPolyline"
            and not GeometryBuilder.are_adjacent_polyline_segments(
                first["element"],
                first["index"],
                record["index"],
            )
        ):
            message = (
                "FILLET: dentro de una misma PLINE, "
                "los segmentos deben ser adyacentes"
            )
            print(message)
            self._status(canvas, message)
            return

        result = GeometryBuilder.create_fillet_from_lines(
            first["segment"],
            record["segment"],
            first["pick"],
            record["pick"],
            self.radius,
        )

        if result is None:
            message = (
                "FILLET: geometría paralela, colineal "
                "o empalme no válido"
            )
            print(message)
            self._status(canvas, message)
            return

        new_first, new_second, arc = result
        originals = []
        replacements = []

        first_element = first["element"]
        second_element = record["element"]

        # Dos segmentos de la misma PLINE.
        if first_element is second_element:
            source = first_element
            first_index = first["index"]
            second_index = record["index"]

            first_line = GeometryBuilder.orient_line_like(
                first["segment"],
                new_first.geometry,
            )
            second_line = GeometryBuilder.orient_line_like(
                record["segment"],
                new_second.geometry,
            )

            replacement_map = {
                first_index: first_line,
                second_index: second_line,
            }
            insertions = {}

            if arc is not None:
                # Inserta el arco entre los dos segmentos conforme
                # al orden de la PLINE.
                lower = min(first_index, second_index)
                upper = max(first_index, second_index)

                if upper - lower == 1:
                    insertions[lower] = [arc]
                else:
                    # Caso esquina de cierre.
                    insertions[max(first_index, second_index)] = [arc]

            new_polyline = GeometryBuilder.replace_polyline_segments(
                source,
                replacement_map,
                insertions,
            )
            originals = [source]
            replacements = [new_polyline]

        else:
            replacement_by_element = {}

            for pick_record, new_line in (
                (first, new_first),
                (record, new_second),
            ):
                element = pick_record["element"]

                if element.__class__.__name__ == "CadPolyline":
                    oriented = GeometryBuilder.orient_line_like(
                        pick_record["segment"],
                        new_line.geometry,
                    )
                    replacement_by_element[element] = (
                        GeometryBuilder.replace_polyline_segments(
                            element,
                            {pick_record["index"]: oriented},
                        )
                    )
                else:
                    replacement_by_element[element] = new_line

            originals = list(replacement_by_element.keys())
            replacements = list(replacement_by_element.values())

            if arc is not None:
                replacements.append(arc)

        scene = self._scene(canvas)

        for element in originals:
            scene.remove_element(element)

        for element in replacements:
            scene.add_element(element)

        if self.app_core is not None:
            self.app_core.history.push(
                FilletAction(
                    scene,
                    originals,
                    replacements,
                )
            )

        print(
            f"FILLET completado: radio={self.radius:g}"
        )

        self.first_pick_record = None
        canvas.preview_geometry = None
        canvas.highlight.clear()
        canvas.element_selected.emit(None)
        canvas.update()
        self._prompt(
            canvas,
            "Seleccione primer segmento o escriba R:",
        )
        self._status(
            canvas,
            "FILLET completado; comando permanece activo",
        )

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()

        if not value:
            return False

        if value.upper() in {"R", "RADIO", "RADIUS"}:
            self.awaiting_radius = True
            self._prompt(canvas, "Especifique radio FILLET:")
            return True

        if self.awaiting_radius:
            try:
                radius = float(value.replace(",", "."))
            except ValueError:
                self._status(canvas, "FILLET: radio no válido")
                return True

            if radius < 0.0:
                self._status(
                    canvas,
                    "FILLET: el radio no puede ser negativo",
                )
                return True

            self.radius = radius
            self.awaiting_radius = False
            print(f"FILLET: radio={self.radius:g}")
            self._prompt(canvas, "Seleccione primer segmento:")
            return True

        try:
            radius = float(value.replace(",", "."))
        except ValueError:
            return False

        if radius < 0.0:
            self._status(
                canvas,
                "FILLET: el radio no puede ser negativo",
            )
            return True

        self.radius = radius
        print(f"FILLET: radio={self.radius:g}")
        return True

    def cancel(self, canvas=None):
        self.first_pick_record = None
        self.awaiting_radius = False

        if canvas is not None:
            canvas.preview_geometry = None
            canvas.highlight.clear()
            canvas.update()
            self._prompt(canvas, "Comando:")
            self._status(canvas, "FILLET cancelado")

        print("FILLET cancelado")

    def deactivate(self):
        self.first_pick_record = None
        self.awaiting_radius = False
        print("FILLET desactivado")
