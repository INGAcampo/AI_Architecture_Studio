"""
AI Architecture Studio
CAD Engine - Mouse Controller

Versión: Alpha 0.6
"""

from PySide6.QtCore import Qt

from engines.cad.coordinates import CoordinateSystem


class MouseController:

    def __init__(self, canvas):

        self.canvas = canvas

        self.mouse_x = 0
        self.mouse_y = 0

        self.coordinates = CoordinateSystem()


    def mouse_move(self, event):

        self.mouse_x = event.position().x()
        self.mouse_y = event.position().y()


        world_x, world_y = self.coordinates.screen_to_world(
            self.mouse_x,
            self.mouse_y,
            self.canvas.camera
        )


        self.canvas.cursor_position = (
            world_x,
            world_y
        )


        self.canvas.update()


    def mouse_press(self, event):

        if event.button() == Qt.LeftButton:

            print(
                "Punto seleccionado:",
                self.canvas.cursor_position
            )


    def wheel(self, event):

        delta = event.angleDelta().y()


        if delta > 0:
            self.canvas.camera.zoom_at(1.10)

        else:
            self.canvas.camera.zoom_at(0.90)


        self.canvas.update()