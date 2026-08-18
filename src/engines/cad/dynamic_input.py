"""
AI Architecture Studio
CAD Engine - Dynamic Input Professional

Package 2.5.1
Corrección compatible de begin_edit(character=None)

Compatibilidad:
- Llamadas antiguas: begin_edit()
- Entrada directa: begin_edit(character)
- Alias: input_character(character)
- Alias: handle_character(character)
- Punto decimal y coma decimal
- Teclado numérico con ";" convertido a ","
"""

import math

from engines.geometry.point import Point


class DynamicField:
    DISTANCE = "distance"
    ANGLE = "angle"

    def __init__(self, field_type, label):
        self.field_type = field_type
        self.label = label
        self.value = ""
        self.active = False
        self.visible = True

    def clear(self):
        self.value = ""

    def numeric_value(self):
        text = str(self.value or "").strip()

        if not text:
            return None

        # En campos simples de distancia o ángulo, la coma funciona
        # como separador decimal.
        if (
            "," in text
            and "@" not in text
            and "<" not in text
        ):
            text = text.replace(",", ".")

        try:
            return float(text)
        except (TypeError, ValueError):
            return None


class DynamicInputManager:
    MODE_DISTANCE = DynamicField.DISTANCE
    MODE_ANGLE = DynamicField.ANGLE

    def __init__(self):
        self.enabled = True
        self.visible = False
        self.base_point = None
        self.current_point = None
        self.distance = 0.0
        self.angle_degrees = 0.0

        self.distance_field = DynamicField(
            DynamicField.DISTANCE,
            "Distancia",
        )
        self.angle_field = DynamicField(
            DynamicField.ANGLE,
            "Ángulo",
        )

        self.active_mode = self.MODE_DISTANCE
        self.distance_field.active = True

        self.screen_x = 0
        self.screen_y = 0
        self.prompt = ""

        # Compatibilidad con versiones anteriores.
        self.typed_value = ""
        self.input_buffer = ""
        self.editing = False
        self.confirmed = False
        self.last_confirmed_value = None

    def toggle(self):
        self.enabled = not self.enabled

        if not self.enabled:
            self.hide()

        state = "ACTIVADO" if self.enabled else "DESACTIVADO"
        print(f"DYNAMIC INPUT {state}")
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
        self.editing = False

    def reset_fields(self):
        self.distance_field.clear()
        self.angle_field.clear()
        self.editing = False
        self.activate_distance()

    def reset(self):
        self.visible = False
        self.base_point = None
        self.current_point = None
        self.distance = 0.0
        self.angle_degrees = 0.0
        self.prompt = ""
        self.confirmed = False
        self.last_confirmed_value = None
        self.reset_fields()

    def set_base_point(self, point):
        if point is None:
            self.base_point = None
            self.hide()
            return

        changed = (
            self.base_point is None
            or self.base_point.distance_to(point) > 1.0e-9
        )

        self.base_point = point

        if changed:
            self.reset_fields()

        self.show()

    def update_point(self, point):
        self.current_point = point

        if self.base_point is None or point is None:
            self.distance = 0.0
            self.angle_degrees = 0.0
            return

        dx = point.x - self.base_point.x
        dy = point.y - self.base_point.y

        self.distance = math.hypot(dx, dy)
        self.angle_degrees = (
            math.degrees(math.atan2(dy, dx)) % 360.0
        )
        self.show()

    def set_screen_position(
        self,
        x,
        y,
        offset_x=18,
        offset_y=-28,
    ):
        self.screen_x = int(x + offset_x)
        self.screen_y = int(y + offset_y)

    def set_cursor_position(self, x, y):
        self.set_screen_position(x, y)

    def active_field(self):
        if self.active_mode == self.MODE_ANGLE:
            return self.angle_field

        return self.distance_field

    def _sync_text(self):
        self.typed_value = self.active_field().value
        self.input_buffer = self.typed_value

    def activate_distance(self):
        self.active_mode = self.MODE_DISTANCE
        self.distance_field.active = True
        self.angle_field.active = False
        self._sync_text()
        return self.active_mode

    def activate_angle(self):
        self.active_mode = self.MODE_ANGLE
        self.distance_field.active = False
        self.angle_field.active = True
        self._sync_text()
        return self.active_mode

    def next_field(self):
        if self.active_mode == self.MODE_DISTANCE:
            return self.activate_angle()

        return self.activate_distance()

    def previous_field(self):
        return self.next_field()

    def toggle_mode(self):
        return self.next_field()

    def set_mode(self, mode):
        if mode == self.MODE_DISTANCE:
            self.activate_distance()
        elif mode == self.MODE_ANGLE:
            self.activate_angle()
        else:
            raise ValueError(
                f"Modo Dynamic Input inválido: {mode}"
            )

    def set_prompt(self, prompt):
        self.prompt = str(prompt or "")

    def set_typed_value(self, value):
        self.active_field().value = str(value or "")
        self._sync_text()
        self.editing = bool(self.typed_value)

    def clear_typed_value(self):
        self.active_field().clear()
        self._sync_text()

    def clear_all_values(self):
        self.distance_field.clear()
        self.angle_field.clear()
        self._sync_text()
        self.editing = False

    def begin_edit(self, character=None):
        """
        Inicia el modo de edición.

        Es compatible con las dos formas usadas por versiones anteriores:

            begin_edit()
            begin_edit(character)

        Cuando no se recibe un carácter, solamente activa la edición.
        Cuando se recibe un carácter, lo valida y lo agrega al campo activo.
        """
        self.editing = True
        self.show()

        if character is None:
            return True

        character = str(character)

        if not character:
            return False

        # Algunos teclados numéricos entregan ";" en lugar de coma.
        if character == ";":
            character = ","

        field = self.active_field()
        current = field.value

        if self.active_mode == self.MODE_ANGLE:
            if character not in "0123456789.,+-":
                return False

            # En el campo de ángulo, coma y punto son decimales.
            if character in ".,":
                if "." in current or "," in current:
                    return True

            if character in "+-" and current:
                return True

        else:
            if character not in "0123456789.,@<+-":
                return False

            # "@" solo puede aparecer al principio.
            if character == "@" and current:
                return True

            # No permitir más de un marcador polar.
            if character == "<" and "<" in current:
                return True

            # Después de "<", la coma se interpreta como decimal
            # del ángulo; antes de "<" puede representar decimal o
            # separador cartesiano según CoordinateParser.
            if character == "," and "<" in current:
                angle_part = current.split("<", 1)[1]
                if "," in angle_part or "." in angle_part:
                    return True

            # Solo un signo inicial o un signo después de "<".
            if character in "+-":
                if not current:
                    pass
                elif current.endswith("<"):
                    pass
                else:
                    return True

        field.value = current + character
        self._sync_text()
        self.editing = True
        self.show()
        return True

    def input_character(self, character):
        """Alias estable para introducir un carácter."""
        return self.begin_edit(character)

    def handle_character(self, character):
        """Alias compatible con otros controladores de teclado."""
        return self.begin_edit(character)

    def append_character(self, character):
        """Alias adicional para integraciones antiguas."""
        return self.begin_edit(character)

    def backspace(self):
        field = self.active_field()

        if not field.value:
            return False

        field.value = field.value[:-1]
        self._sync_text()
        self.editing = bool(
            self.distance_field.value
            or self.angle_field.value
        )
        return True

    def cancel_edit(self):
        self.clear_all_values()

    def _normalize_decimal_field(self, text):
        value = str(text or "").strip()

        if (
            "," in value
            and "@" not in value
            and "<" not in value
        ):
            value = value.replace(",", ".")

        return value

    def confirmation_text(self):
        distance_text = self.distance_field.value.strip()
        angle_text = self.angle_field.value.strip()

        if angle_text:
            if not distance_text:
                distance_text = f"{self.distance:.6f}"

            distance_text = self._normalize_decimal_field(
                distance_text
            )
            angle_text = self._normalize_decimal_field(
                angle_text
            )

            return f"@{distance_text}<{angle_text}"

        # Conserva los formatos históricos:
        # 12.5, 12,5, 10,10, @10,5, @10<45 y 10<45.
        return distance_text

    def confirm(self):
        text = self.confirmation_text().strip()

        if not text:
            return None

        self.confirmed = True
        self.last_confirmed_value = text
        self.editing = False
        return text

    def consume_confirmed_value(self):
        value = self.last_confirmed_value
        self.last_confirmed_value = None
        self.confirmed = False
        return value

    def constrained_values(self):
        distance = self.distance_field.numeric_value()
        angle = self.angle_field.numeric_value()

        if distance is None:
            distance = self.distance

        if angle is None:
            angle = self.angle_degrees

        return distance, angle

    def constrained_point(self, base_point=None):
        origin = base_point or self.base_point

        if origin is None:
            return self.current_point

        distance, angle = self.constrained_values()
        radians = math.radians(angle)

        return Point(
            origin.x + distance * math.cos(radians),
            origin.y + distance * math.sin(radians),
            origin.z,
        )

    def formatted_distance(self):
        return f"{self.distance:.3f}"

    def formatted_angle(self):
        return f"{self.angle_degrees:.1f}°"

    def distance_display_text(self):
        return (
            self.distance_field.value
            or self.formatted_distance()
        )

    def angle_display_text(self):
        return (
            self.angle_field.value
            or self.formatted_angle()
        )

    def primary_text(self):
        return self.distance_display_text()

    def secondary_text(self):
        return self.angle_display_text()

    def snapshot(self):
        return {
            "enabled": self.enabled,
            "visible": self.visible,
            "distance": self.distance,
            "angle_degrees": self.angle_degrees,
            "active_mode": self.active_mode,
            "distance_text": self.distance_field.value,
            "angle_text": self.angle_field.value,
            "screen_x": self.screen_x,
            "screen_y": self.screen_y,
        }