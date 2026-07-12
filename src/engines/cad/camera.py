"""
AI Architecture Studio
CAD Engine - Camera

Versión: Alpha 0.5
"""


class Camera:
    def __init__(self):
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

    def world_to_screen(self, x, y):
        screen_x = x * self.zoom + self.offset_x
        screen_y = y * self.zoom + self.offset_y
        return screen_x, screen_y

    def screen_to_world(self, x, y):
        world_x = (x - self.offset_x) / self.zoom
        world_y = (y - self.offset_y) / self.zoom
        return world_x, world_y

    def pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def zoom_at(self, factor):
        self.zoom *= factor

        if self.zoom < 0.1:
            self.zoom = 0.1

        if self.zoom > 10:
            self.zoom = 10