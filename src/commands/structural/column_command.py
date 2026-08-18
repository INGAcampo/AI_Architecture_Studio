class ColumnCommand:

    ALIASES = [
        "COLUMN",
        "COL",
    ]

    DEFAULT_WIDTH = 0.30
    DEFAULT_DEPTH = 0.30
    DEFAULT_DIAMETER = 0.30
    DEFAULT_HEIGHT = 3.00

    def begin(self, canvas):
        print("COLUMN activado")

    def mouse_press(self, event, canvas):
        pass
