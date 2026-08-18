"""
AI Architecture Studio
JOIN Professional 4.3

Flujos:
1. Preselecciona dos o más LINE/PLINE y ejecuta JOIN.
2. Ejecuta JOIN y selecciona entidades consecutivamente.
   La unión se procesa al seleccionar la segunda entidad.
3. Escribe T para cambiar la tolerancia.
"""

from commands.base_command import BaseCommand
from core.history.join_action import JoinAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class JoinCommand(BaseCommand):

    PICK_TOLERANCE = 0.55

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "JOIN"
        self.tolerance = 0.01
        self.collected = []
        self.awaiting_tolerance = False

    def _scene(self, canvas):
        return getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

    def _window(self, canvas):
        getter = getattr(canvas, "window", None)
        return getter() if callable(getter) else None

    def _status(self, canvas, text):
        window = self._window(canvas)
        if window is not None:
            window.statusBar().showMessage(text)

    def _prompt(self, canvas, text):
        window = self._window(canvas)
        command_line = getattr(window, "command_line", None)
        if command_line is not None:
            command_line.set_prompt(text)

    def _canvas_point(self, canvas):
        getter = getattr(canvas, "get_input_point", None)
        if callable(getter):
            return getter()
        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    def _selected_elements(self, canvas):
        manager = getattr(canvas, "selection_manager", None)
        if manager is None:
            return []

        getter = getattr(manager, "selected_elements", None)
        if not callable(getter):
            return []

        return [
            element
            for element in getter()
            if GeometryBuilder.can_join_element(element)
        ]

    def activate(self):
        super().activate()
        print(
            "JOIN activo: preselecciona o selecciona "
            "LINE/PLINE conectadas; escribe T para tolerancia"
        )

    def begin(self, canvas):
        """
        ToolManager puede llamar begin() tras activate().
        Si existe preselección válida, JOIN se ejecuta inmediatamente.
        """
        selected = self._selected_elements(canvas)

        if len(selected) >= 2:
            self.collected = selected
            self._execute(canvas)
            return

        self._prompt(
            canvas,
            "Seleccione primera LINE/PLINE o escriba T:",
        )

    def _distance_to_element(self, element, point):
        geometry = getattr(element, "geometry", None)

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return GeometryBuilder.distance_to_line_segment(
                geometry,
                point,
            )

        if element.__class__.__name__ == "CadPolyline":
            distances = [
                GeometryBuilder.distance_to_line_segment(
                    segment,
                    point,
                )
                for _, segment in (
                    GeometryBuilder.polyline_segment_records(
                        element
                    )
                )
            ]

            # Las PLINE híbridas pueden incluir arcos. Para JOIN
            # basta con seleccionar cualquier tramo recto visible.
            if distances:
                return min(distances)

        return None

    def _find_target(self, canvas, point):
        scene = self._scene(canvas)

        if scene is None:
            return None

        candidates = []

        for element in scene.get_elements():
            if element in self.collected:
                continue

            if not GeometryBuilder.can_join_element(element):
                continue

            distance = self._distance_to_element(element, point)

            if distance is not None:
                candidates.append((distance, element))

        candidates.sort(key=lambda item: item[0])

        if (
            not candidates
            or candidates[0][0] > self.PICK_TOLERANCE
        ):
            return None

        return candidates[0][1]

    def mouse_move(self, event, canvas):
        point = self._canvas_point(canvas)
        target = self._find_target(canvas, point)

        canvas.highlight.clear()

        if target is not None:
            canvas.highlight.set(target)

        canvas.update()

    def mouse_press(self, event, canvas):
        point = self._canvas_point(canvas)
        target = self._find_target(canvas, point)

        if target is None:
            message = (
                "JOIN: no se encontró una LINE o PLINE "
                "cerca del cursor"
            )
            print(message)
            self._status(canvas, message)
            return

        self.collected.append(target)
        print(
            f"JOIN: {len(self.collected)} objeto(s) seleccionado(s)"
        )

        if len(self.collected) == 1:
            self._prompt(
                canvas,
                "Seleccione segunda LINE/PLINE:",
            )
            return

        self._execute(canvas)

    def _execute(self, canvas):
        replacement = GeometryBuilder.create_joined_polyline(
            self.collected,
            tolerance=self.tolerance,
        )

        if replacement is None:
            message = (
                "JOIN: las entidades no forman una cadena "
                "continua dentro de la tolerancia"
            )
            print(message)
            self._status(canvas, message)

            # Conserva el último elemento como inicio de una nueva
            # cadena y evita bloquear el comando.
            self.collected = self.collected[-1:]
            canvas.highlight.clear()
            canvas.update()
            return False

        originals = list(self.collected)
        scene = self._scene(canvas)

        for element in originals:
            scene.remove_element(element)

        scene.add_element(replacement)

        if self.app_core is not None:
            self.app_core.history.push(
                JoinAction(
                    scene,
                    originals,
                    replacement,
                )
            )

        state = "cerrada" if replacement.closed else "abierta"
        print(
            f"JOIN completado: {len(originals)} objeto(s) "
            f"→ 1 PLINE {state}"
        )

        self.collected = []
        canvas.highlight.clear()
        canvas.selection_manager.clear()
        canvas.element_selected.emit(None)
        canvas.update()

        self._status(
            canvas,
            f"JOIN completado: PLINE {state}",
        )
        self._prompt(
            canvas,
            "Seleccione primera LINE/PLINE:",
        )
        return True

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()

        if value.upper() in {"T", "TOL", "TOLERANCIA"}:
            self.awaiting_tolerance = True
            self._prompt(
                canvas,
                "Especifique tolerancia JOIN:",
            )
            return True

        if self.awaiting_tolerance:
            try:
                tolerance = float(value.replace(",", "."))
            except ValueError:
                self._status(
                    canvas,
                    "JOIN: tolerancia no válida",
                )
                return True

            if tolerance < 0.0:
                self._status(
                    canvas,
                    "JOIN: la tolerancia no puede ser negativa",
                )
                return True

            self.tolerance = tolerance
            self.awaiting_tolerance = False
            print(f"JOIN: tolerancia={self.tolerance:g}")
            self._prompt(
                canvas,
                "Seleccione primera LINE/PLINE:",
            )
            return True

        if value.upper() in {"ENTER", "FINALIZAR", "FIN"}:
            if len(self.collected) >= 2:
                return self._execute(canvas)

            self._status(
                canvas,
                "JOIN: selecciona al menos dos entidades",
            )
            return True

        return False

    def cancel(self, canvas=None):
        self.collected = []
        self.awaiting_tolerance = False

        if canvas is not None:
            canvas.highlight.clear()
            canvas.update()
            self._prompt(canvas, "Comando:")
            self._status(canvas, "JOIN cancelado")

        print("JOIN cancelado")

    def deactivate(self):
        self.collected = []
        self.awaiting_tolerance = False
        print("JOIN desactivado")
