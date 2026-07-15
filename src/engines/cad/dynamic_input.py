"""
AI Architecture Studio
CAD Engine - Dynamic Input

Dynamic Input v2
"""

import math


class DynamicInputManager:
    """
    Mantiene el estado del panel flotante de entrada dinámica.

    En esta primera etapa no procesa teclado directamente.
    Solo calcula y expone:

    - punto base;
    - punto actual;
    - distancia;
    - ángulo;
    - texto de estado;
    - posición del panel;
    - activación con F12.
    """

    MODE_DISTANCE = "distance"
    MODE_ANGLE = "angle"

    def __init__(self):
        self.enabled = True
        self.visible = False

        self.base_point = None
        self.current_point = None

        self.distance = 0.0
        self.angle_degrees = 0.0

        self.active_mode = self.MODE_DISTANCE

        self.screen_x = 0
        self.screen_y = 0

        self.prompt = ""
        self.typed_value = ""

    # ---------------------------------------------------------
    # ESTADO GENERAL
    # ---------------------------------------------------------

    def toggle(self):
        self.enabled = not self.enabled

        if not self.enabled:
            self.hide()

        state = (
            "ACTIVADO"
            if self.enabled
            else "DESACTIVADO"
        )

        print(
            f"DYNAMIC INPUT {state}"
        )

        return self.enabled

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)

        if not self.enabled:
            self.hide()

    def show(self):
        if self.enabled:
            self.visible = True

    def hide(self):
        self.visible = False
        self.typed_value = ""

    def reset(self):
        self.visible = False

        self.base_point = None
        self.current_point = None

        self.distance = 0.0
        self.angle_degrees = 0.0

        self.active_mode = self.MODE_DISTANCE

        self.prompt = ""
        self.typed_value = ""

    # ---------------------------------------------------------
    # PUNTOS Y MEDICIONES
    # ---------------------------------------------------------

    def set_base_point(self, point):
        self.base_point = point

        if point is None:
            self.hide()
            return

        self.show()

    def update_point(self, point):
        self.current_point = point

        if (
            not self.enabled
            or self.base_point is None
            or point is None
        ):
            self.distance = 0.0
            self.angle_degrees = 0.0
            return

        dx = (
            point.x
            - self.base_point.x
        )

        dy = (
            point.y
            - self.base_point.y
        )

        self.distance = math.hypot(
            dx,
            dy,
        )

        self.angle_degrees = (
            math.degrees(
                math.atan2(
                    dy,
                    dx,
                )
            )
            % 360.0
        )

        self.show()

    # ---------------------------------------------------------
    # POSICIÓN EN PANTALLA
    # ---------------------------------------------------------

    def set_screen_position(
        self,
        x,
        y,
        offset_x=18,
        offset_y=-28,
    ):
        self.screen_x = int(
            x + offset_x
        )

        self.screen_y = int(
            y + offset_y
        )

    # ---------------------------------------------------------
    # MODOS
    # ---------------------------------------------------------

    def toggle_mode(self):
        if (
            self.active_mode
            == self.MODE_DISTANCE
        ):
            self.active_mode = (
                self.MODE_ANGLE
            )
        else:
            self.active_mode = (
                self.MODE_DISTANCE
            )

        return self.active_mode

    def set_mode(self, mode):
        if mode not in (
            self.MODE_DISTANCE,
            self.MODE_ANGLE,
        ):
            raise ValueError(
                f"Modo de entrada dinámica "
                f"no válido: {mode}"
            )

        self.active_mode = mode

    # ---------------------------------------------------------
    # TEXTO
    # ---------------------------------------------------------

    def set_prompt(self, prompt):
        self.prompt = str(
            prompt or ""
        )

    def set_typed_value(self, value):
        self.typed_value = str(
            value or ""
        )

    def clear_typed_value(self):
        self.typed_value = ""

    # ---------------------------------------------------------
    # FORMATO
    # ---------------------------------------------------------

    def formatted_distance(self):
        return f"{self.distance:.3f}"

    def formatted_angle(self):
        return (
            f"{self.angle_degrees:.2f}°"
        )

    def primary_text(self):
        if (
            self.active_mode
            == self.MODE_ANGLE
        ):
            return self.formatted_angle()

        return self.formatted_distance()

    def secondary_text(self):
        if (
            self.active_mode
            == self.MODE_ANGLE
        ):
            return self.formatted_distance()

        return self.formatted_angle()

    def snapshot(self):
        return {
            "enabled": self.enabled,
            "visible": self.visible,
            "base_point": self.base_point,
            "current_point": self.current_point,
            "distance": self.distance,
            "angle_degrees": (
                self.angle_degrees
            ),
            "active_mode": (
                self.active_mode
            ),
            "screen_position": (
                self.screen_x,
                self.screen_y,
            ),
            "prompt": self.prompt,
            "typed_value": (
                self.typed_value
            ),
        }