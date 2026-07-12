"""
AI Architecture Studio
Base Command

CAD Professional Framework
"""


class BaseCommand:
    def __init__(self, app_core=None):
        self.app_core = app_core
        self.name = "COMMAND"
        self.active = False

    def activate(self):
        self.active = True
        print(f"{self.name} activado")

    def deactivate(self):
        self.active = False
        print(f"{self.name} desactivado")

    def mouse_press(self, event, canvas):
        pass

    def mouse_move(self, event, canvas):
        pass

    def mouse_release(self, event, canvas):
        pass

    def key_press(self, event, canvas):
        pass

    def finish(self, canvas):
        self.deactivate()

    def cancel(self, canvas):
        self.deactivate()