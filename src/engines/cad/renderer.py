from PySide6.QtGui import QPen, QColor

from engines.cad.coordinates import CoordinateSystem


class Renderer:

    def __init__(self):

        self.default_pen = QPen(QColor(220, 220, 220), 2)
        self.preview_pen = QPen(QColor(80, 220, 120), 1)
        self.highlight_pen = QPen(QColor(255, 210, 0), 3)

        self.coordinates = CoordinateSystem()

    def draw_line(
        self,
        painter,
        camera,
        line,
        preview=False,
        highlighted=False
    ):

        if highlighted:
            painter.setPen(self.highlight_pen)
        elif preview:
            painter.setPen(self.preview_pen)
        else:
            painter.setPen(self.default_pen)

        x1, y1 = self.coordinates.world_to_screen(
            line.start.x,
            line.start.y,
            camera
        )

        x2, y2 = self.coordinates.world_to_screen(
            line.end.x,
            line.end.y,
            camera
        )

        painter.drawLine(
            int(x1),
            int(y1),
            int(x2),
            int(y2)
        )

    def draw_polyline(
        self,
        painter,
        camera,
        polyline,
        highlighted=False
    ):

        painter.setPen(
            self.highlight_pen
            if highlighted
            else self.default_pen
        )

        points = polyline.points

        if len(points) < 2:
            return

        for index in range(len(points) - 1):

            point_1 = points[index]
            point_2 = points[index + 1]

            x1, y1 = self.coordinates.world_to_screen(
                point_1.x,
                point_1.y,
                camera
            )

            x2, y2 = self.coordinates.world_to_screen(
                point_2.x,
                point_2.y,
                camera
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            )

        if polyline.closed and len(points) > 2:

            point_1 = points[-1]
            point_2 = points[0]

            x1, y1 = self.coordinates.world_to_screen(
                point_1.x,
                point_1.y,
                camera
            )

            x2, y2 = self.coordinates.world_to_screen(
                point_2.x,
                point_2.y,
                camera
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            )

    def draw_circle(
        self,
        painter,
        camera,
        circle,
        preview=False,
        highlighted=False
    ):

        if highlighted:
            painter.setPen(self.highlight_pen)
        elif preview:
            painter.setPen(self.preview_pen)
        else:
            painter.setPen(self.default_pen)

        center_x, center_y = self.coordinates.world_to_screen(
            circle.center.x,
            circle.center.y,
            camera
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
            int(radius_pixels * 2)
        )

    def draw_preview(
        self,
        painter,
        camera,
        preview_geometry
    ):

        if preview_geometry is None:
            return

        preview_type = preview_geometry.__class__.__name__

        if preview_type == "Line":
            self.draw_line(
                painter,
                camera,
                preview_geometry,
                preview=True
            )

        elif preview_type == "CadCircle":
            self.draw_circle(
                painter,
                camera,
                preview_geometry,
                preview=True
            )

    def draw_scene(
        self,
        painter,
        camera,
        scene,
        highlighted=None
    ):

        if scene is None:
            return

        for element in scene.get_elements():

            geometry = getattr(
                element,
                "geometry",
                None
            )

            is_highlighted = (
                highlighted is not None
                and highlighted == element
            )

            if (
                geometry
                and geometry.__class__.__name__ == "Line"
            ):

                self.draw_line(
                    painter,
                    camera,
                    geometry,
                    highlighted=is_highlighted
                )

            elif element.__class__.__name__ == "CadPolyline":

                self.draw_polyline(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted
                )

            elif element.__class__.__name__ == "CadRectangle":

                self.draw_polyline(
                    painter,
                    camera,
                    element.polyline,
                    highlighted=is_highlighted
                )

            elif element.__class__.__name__ == "CadCircle":

                self.draw_circle(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted
                )