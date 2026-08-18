"""
AI Architecture Studio
CHAMFER Professional 4.2

Soporta:
- LINE ↔ LINE
- dos segmentos adyacentes de la misma PLINE
- LINE ↔ segmento PLINE
- segmento PLINE ↔ segmento PLINE
- distancias independientes, modo simétrico y distancia cero
"""

from commands.base_command import BaseCommand
from core.history.chamfer_action import ChamferAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.line import Line
from engines.geometry.point import Point


class ChamferCommand(BaseCommand):

    PICK_TOLERANCE = 0.55

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "CHAMFER"
        self.first_distance = 1.0
        self.second_distance = 1.0
        self.first_pick_record = None
        self.input_state = None

    def activate(self):
        super().activate()
        print(
            "CHAMFER activo: distancias=1,1. "
            "Selecciona LINE o segmento de PLINE; escribe D o S"
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
                records.append(
                    {
                        "element": element,
                        "segment": geometry,
                        "index": None,
                        "distance": GeometryBuilder.distance_to_line_segment(
                            geometry,
                            point,
                        ),
                        "pick": point,
                    }
                )
                continue

            if element.__class__.__name__ == "CadPolyline":
                for index, segment in (
                    GeometryBuilder.polyline_segment_records(element)
                ):
                    records.append(
                        {
                            "element": element,
                            "segment": segment,
                            "index": index,
                            "distance": GeometryBuilder.distance_to_line_segment(
                                segment,
                                point,
                            ),
                            "pick": point,
                        }
                    )

        return sorted(records, key=lambda item: item["distance"])

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

    def _preview_line(self, result):
        if result is None:
            return None

        _, _, chamfer = result

        if chamfer is None:
            return None

        return chamfer.geometry

    def mouse_move(self, event, canvas):
        point = self._canvas_point(canvas)
        record = self._find_record(canvas, point)

        canvas.highlight.clear()
        canvas.preview_geometry = None

        if record is not None:
            canvas.highlight.set(record["element"])

            if self.first_pick_record is not None:
                result = GeometryBuilder.create_chamfer_from_lines(
                    self.first_pick_record["segment"],
                    record["segment"],
                    self.first_pick_record["pick"],
                    point,
                    self.first_distance,
                    self.second_distance,
                )
                canvas.preview_geometry = self._preview_line(result)

        canvas.update()

    @staticmethod
    def _oriented_connector(first_line, second_line):
        return Line(
            GeometryBuilder._copy_point(first_line.end),
            GeometryBuilder._copy_point(second_line.start),
        )

    def mouse_press(self, event, canvas):
        point = self._canvas_point(canvas)
        record = self._find_record(canvas, point)

        if record is None:
            message = (
                "CHAMFER: no se encontró una LINE o segmento "
                "recto de PLINE cerca del cursor"
            )
            print(message)
            self._status(canvas, message)
            return

        record["pick"] = point

        if self.first_pick_record is None:
            self.first_pick_record = record
            print("CHAMFER: primer segmento seleccionado")
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
                "CHAMFER: dentro de una misma PLINE, "
                "los segmentos deben ser adyacentes"
            )
            print(message)
            self._status(canvas, message)
            return

        result = GeometryBuilder.create_chamfer_from_lines(
            first["segment"],
            record["segment"],
            first["pick"],
            record["pick"],
            self.first_distance,
            self.second_distance,
        )

        if result is None:
            message = (
                "CHAMFER: geometría paralela, colineal "
                "o chaflán no válido"
            )
            print(message)
            self._status(canvas, message)
            return

        new_first, new_second, connector = result
        originals = []
        replacements = []
        first_element = first["element"]
        second_element = record["element"]

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

            if connector is not None:
                lower = min(first_index, second_index)
                upper = max(first_index, second_index)

                if upper - lower == 1:
                    lower_line = replacement_map[lower]
                    upper_line = replacement_map[upper]
                    insertions[lower] = [
                        self._oriented_connector(
                            lower_line,
                            upper_line,
                        )
                    ]
                else:
                    # Esquina de cierre: último segmento -> primero.
                    last_line = replacement_map[max(first_index, second_index)]
                    first_line_ordered = replacement_map[min(first_index, second_index)]
                    insertions[max(first_index, second_index)] = [
                        self._oriented_connector(
                            last_line,
                            first_line_ordered,
                        )
                    ]

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

            if connector is not None:
                replacements.append(connector)

        scene = self._scene(canvas)

        for element in originals:
            scene.remove_element(element)

        for element in replacements:
            scene.add_element(element)

        if self.app_core is not None:
            self.app_core.history.push(
                ChamferAction(scene, originals, replacements)
            )

        print(
            "CHAMFER completado: "
            f"distancias={self.first_distance:g},"
            f"{self.second_distance:g}"
        )

        self.first_pick_record = None
        canvas.preview_geometry = None
        canvas.highlight.clear()
        canvas.element_selected.emit(None)
        canvas.update()
        self._prompt(
            canvas,
            "Seleccione primer segmento o escriba D/S:",
        )
        self._status(
            canvas,
            "CHAMFER completado; comando permanece activo",
        )

    def _accept_distance(self, value, canvas):
        try:
            distance = float(value.replace(",", "."))
        except ValueError:
            self._status(canvas, "CHAMFER: distancia no válida")
            return None

        if distance < 0.0:
            self._status(
                canvas,
                "CHAMFER: la distancia no puede ser negativa",
            )
            return None

        return distance

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()

        if not value:
            return False

        upper = value.upper()

        if upper in {"D", "DISTANCIA", "DISTANCE"}:
            self.input_state = "distance_1"
            self._prompt(canvas, "Especifique primera distancia:")
            return True

        if upper in {"S", "SIMETRICO", "SIMÉTRICO", "SYMMETRIC"}:
            self.input_state = "symmetric"
            self._prompt(canvas, "Especifique distancia simétrica:")
            return True

        distance = self._accept_distance(value, canvas)

        if distance is None:
            return True

        if self.input_state == "distance_1":
            self.first_distance = distance
            self.input_state = "distance_2"
            self._prompt(canvas, "Especifique segunda distancia:")
            return True

        if self.input_state == "distance_2":
            self.second_distance = distance
            self.input_state = None
            print(
                "CHAMFER: distancias="
                f"{self.first_distance:g},{self.second_distance:g}"
            )
            self._prompt(canvas, "Seleccione primer segmento:")
            return True

        if self.input_state == "symmetric":
            self.first_distance = distance
            self.second_distance = distance
            self.input_state = None
            print(f"CHAMFER: distancia simétrica={distance:g}")
            self._prompt(canvas, "Seleccione primer segmento:")
            return True

        # Entrada numérica directa: modo simétrico rápido.
        self.first_distance = distance
        self.second_distance = distance
        print(f"CHAMFER: distancia simétrica={distance:g}")
        return True

    def cancel(self, canvas=None):
        self.first_pick_record = None
        self.input_state = None

        if canvas is not None:
            canvas.preview_geometry = None
            canvas.highlight.clear()
            canvas.update()
            self._prompt(canvas, "Comando:")
            self._status(canvas, "CHAMFER cancelado")

        print("CHAMFER cancelado")

    def deactivate(self):
        self.first_pick_record = None
        self.input_state = None
        print("CHAMFER desactivado")
