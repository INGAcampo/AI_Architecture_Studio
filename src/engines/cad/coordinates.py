"""
AI Architecture Studio
CAD Engine - Coordinate System

Versión: Alpha 0.6
"""


class CoordinateSystem:

    def __init__(self, scale=50):
        """
        scale:
        cantidad de píxeles por unidad del modelo

        Ejemplo:
        1 metro = 50 píxeles
        """

        self.scale = scale


    def world_to_screen(self, x, y, camera):

        screen_x = (
            x * self.scale * camera.zoom
            + camera.offset_x
        )

        screen_y = (
            -y * self.scale * camera.zoom
            + camera.offset_y
        )

        return screen_x, screen_y



    def screen_to_world(self, x, y, camera):

        world_x = (
            x - camera.offset_x
        ) / (
            self.scale * camera.zoom
        )


        world_y = -(
            y - camera.offset_y
        ) / (
            self.scale * camera.zoom
        )


        return world_x, world_y