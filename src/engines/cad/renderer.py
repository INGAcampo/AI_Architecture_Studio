"""
AI Architecture Studio
CAD Renderer

Professional Selection v1
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen

from engines.cad.coordinates import CoordinateSystem


class Renderer:

    def __init__(self):
        self.default_pen = QPen(
            QColor(220, 220, 220),
            2,
        )

        self.preview_pen = QPen(
            QColor(80, 220, 120),
            1,
        )

        self.highlight_pen = QPen(
            QColor(255, 210, 0),
            3,
        )

        self.selection_pen = QPen(
            QColor(0, 170, 255),
            3,
        )

        self.snap_pen = QPen(
            QColor(0, 255, 255),
            2,
        )

        self.window_pen = QPen(
            QColor(60, 150, 255),
            1,
        )

        self.crossing_pen = QPen(
            QColor(70, 220, 120),
            1,
        )

        self.coordinates = CoordinateSystem()

    # ---------------------------------------------------------
    # CONFIGURACIÓN DE PLUMAS
    # ---------------------------------------------------------

    def _set_entity_pen(
        self,
        painter,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        if selected:
            painter.setPen(
                self.selection_pen
            )

        elif highlighted:
            painter.setPen(
                self.highlight_pen
            )

        elif preview:
            painter.setPen(
                self.preview_pen
            )

        else:
            painter.setPen(
                self.default_pen
            )

    # ---------------------------------------------------------
    # LINE
    # ---------------------------------------------------------

    def draw_line(
        self,
        painter,
        camera,
        line,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            preview=preview,
            highlighted=highlighted,
            selected=selected,
        )

        x1, y1 = (
            self.coordinates.world_to_screen(
                line.start.x,
                line.start.y,
                camera,
            )
        )

        x2, y2 = (
            self.coordinates.world_to_screen(
                line.end.x,
                line.end.y,
                camera,
            )
        )

        painter.drawLine(
            int(x1),
            int(y1),
            int(x2),
            int(y2),
        )

    # ---------------------------------------------------------
    # POLYLINE / RECTANGLE
    # ---------------------------------------------------------

    def draw_polyline(
        self,
        painter,
        camera,
        polyline,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            highlighted=highlighted,
            selected=selected,
        )

        points = polyline.points

        if len(points) < 2:
            return

        for index in range(
            len(points) - 1
        ):
            point_1 = points[index]
            point_2 = points[index + 1]

            x1, y1 = (
                self.coordinates.world_to_screen(
                    point_1.x,
                    point_1.y,
                    camera,
                )
            )

            x2, y2 = (
                self.coordinates.world_to_screen(
                    point_2.x,
                    point_2.y,
                    camera,
                )
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2),
            )

        if (
            polyline.closed
            and len(points) > 2
        ):
            point_1 = points[-1]
            point_2 = points[0]

            x1, y1 = (
                self.coordinates.world_to_screen(
                    point_1.x,
                    point_1.y,
                    camera,
                )
            )

            x2, y2 = (
                self.coordinates.world_to_screen(
                    point_2.x,
                    point_2.y,
                    camera,
                )
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2),
            )

    # ---------------------------------------------------------
    # CIRCLE
    # ---------------------------------------------------------

    def draw_circle(
        self,
        painter,
        camera,
        circle,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            preview=preview,
            highlighted=highlighted,
            selected=selected,
        )

        center_x, center_y = (
            self.coordinates.world_to_screen(
                circle.center.x,
                circle.center.y,
                camera,
            )
        )

        radius_pixels = (
            circle.radius
            * self.coordinates.scale
            * camera.zoom
        )

        painter.drawEllipse(
            int(center_x - radius_pixels),
            int(center_y - radius_pixels),
            int(radius_pixels * 2),
            int(radius_pixels * 2),
        )

    # ---------------------------------------------------------
    # SNAP
    # ---------------------------------------------------------

    def draw_snap_marker(
        self,
        painter,
        camera,
        point,
        snap_type,
    ):
        if (
            point is None
            or snap_type is None
        ):
            return

        screen_x, screen_y = (
            self.coordinates.world_to_screen(
                point.x,
                point.y,
                camera,
            )
        )

        x = int(screen_x)
        y = int(screen_y)
        size = 7

        painter.setPen(
            self.snap_pen
        )

        if snap_type == "Endpoint":
            painter.drawRect(
                x - size,
                y - size,
                size * 2,
                size * 2,
            )

        elif snap_type == "Midpoint":
            painter.drawLine(
                x,
                y - size,
                x - size,
                y + size,
            )

            painter.drawLine(
                x - size,
                y + size,
                x + size,
                y + size,
            )

            painter.drawLine(
                x + size,
                y + size,
                x,
                y - size,
            )

        elif snap_type == "Center":
            painter.drawEllipse(
                x - size,
                y - size,
                size * 2,
                size * 2,
            )

            painter.drawLine(
                x - size,
                y,
                x + size,
                y,
            )

            painter.drawLine(
                x,
                y - size,
                x,
                y + size,
            )

        elif snap_type == "Intersection":
            painter.drawLine(
                x - size,
                y - size,
                x + size,
                y + size,
            )

            painter.drawLine(
                x - size,
                y + size,
                x + size,
                y - size,
            )

        elif snap_type == "Nearest":
            painter.drawEllipse(
                x - 4,
                y - 4,
                8,
                8,
            )

        elif snap_type == "Grid":
            painter.drawLine(
                x - size,
                y,
                x + size,
                y,
            )

            painter.drawLine(
                x,
                y - size,
                x,
                y + size,
            )

        painter.drawText(
            x + 12,
            y - 10,
            snap_type,
        )

    # ---------------------------------------------------------
    # VENTANA DE SELECCIÓN
    # ---------------------------------------------------------

    def draw_selection_window(
        self,
        painter,
        camera,
        first_point,
        second_point,
        crossing=False,
    ):
        if (
            first_point is None
            or second_point is None
        ):
            return

        x1, y1 = (
            self.coordinates.world_to_screen(
                first_point.x,
                first_point.y,
                camera,
            )
        )

        x2, y2 = (
            self.coordinates.world_to_screen(
                second_point.x,
                second_point.y,
                camera,
            )
        )

        left = int(
            min(x1, x2)
        )

        top = int(
            min(y1, y2)
        )

        width = max(
            1,
            int(abs(x2 - x1)),
        )

        height = max(
            1,
            int(abs(y2 - y1)),
        )

        if crossing:
            painter.setPen(
                self.crossing_pen
            )

            painter.setBrush(
                QBrush(
                    QColor(
                        50,
                        180,
                        90,
                        45,
                    )
                )
            )

        else:
            painter.setPen(
                self.window_pen
            )

            painter.setBrush(
                QBrush(
                    QColor(
                        50,
                        120,
                        230,
                        45,
                    )
                )
            )

        painter.drawRect(
            left,
            top,
            width,
            height,
        )

        painter.setBrush(
            QBrush(Qt.NoBrush)
        )

    # ---------------------------------------------------------
    # PREVIEW
    # ---------------------------------------------------------

    def draw_preview(
        self,
        painter,
        camera,
        preview_geometry,
    ):
        if preview_geometry is None:
            return

        preview_type = (
            preview_geometry
            .__class__.__name__
        )

        if preview_type == "Line":
            self.draw_line(
                painter,
                camera,
                preview_geometry,
                preview=True,
            )

        elif preview_type == "CadCircle":
            self.draw_circle(
                painter,
                camera,
                preview_geometry,
                preview=True,
            )

    # ---------------------------------------------------------
    # ESCENA
    # ---------------------------------------------------------

    def draw_scene(
        self,
        painter,
        camera,
        scene,
        highlighted=None,
        selected_elements=None,
    ):
        if scene is None:
            return

        selected_elements = set(
            selected_elements or []
        )

        layer_manager = None

        kernel = getattr(
            scene,
            "kernel",
            None,
        )

        if kernel is not None:
            layer_manager = (
                kernel.services.get(
                    "layer_manager"
                )
            )

        for element in scene.get_elements():
            layer_name = getattr(
                element,
                "layer_name",
                "0",
            )

            layer = None

            if layer_manager is not None:
                layer = (
                    layer_manager.get_layer(
                        layer_name
                    )
                )

            if (
                layer is not None
                and not layer.visible
            ):
                continue

            geometry = getattr(
                element,
                "geometry",
                None,
            )

            is_selected = (
                element in selected_elements
            )

            is_highlighted = (
                not is_selected
                and highlighted is not None
                and highlighted == element
            )

            if (
                geometry is not None
                and geometry.__class__.__name__
                == "Line"
            ):
                self.draw_line(
                    painter,
                    camera,
                    geometry,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadPolyline"
            ):
                self.draw_polyline(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadRectangle"
            ):
                self.draw_polyline(
                    painter,
                    camera,
                    element.polyline,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadCircle"
            ):
                self.draw_circle(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )