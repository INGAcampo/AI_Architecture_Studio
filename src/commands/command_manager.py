"""
AI Architecture Studio
Command Manager

Foundation 1.3
"""


class CommandManager:

    def __init__(self):

        self.active_command = None
        self.previous_command = None

    @property
    def active_command_name(self):

        if self.active_command:
            return self.active_command.name

        return "NINGUNO"

    def set_command(self, command):

        if self.active_command:

            self.active_command.deactivate()
            self.previous_command = self.active_command

        self.active_command = command

        if self.active_command:

            self.active_command.activate()

            print(f"Comando actual -> {self.active_command.name}")

    def cancel(self, canvas):

        if self.active_command:

            self.active_command.cancel(canvas)

        self.active_command = None

        print("Comando cancelado")

        canvas.preview_geometry = None
        canvas.update()

    def repeat_last(self):

        return self.previous_command

    def mouse_move(self, event, canvas):

        if self.active_command:

            self.active_command.mouse_move(event, canvas)

    def mouse_press(self, event, canvas):

        if self.active_command:

            self.active_command.mouse_press(event, canvas)

    def key_press(self, event, canvas):

        if self.active_command:

            self.active_command.key_press(event, canvas)

    def wheel(self, event, canvas):

        if self.active_command:

            self.active_command.wheel(event, canvas)