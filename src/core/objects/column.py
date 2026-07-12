from .element import Element


class Column(Element):

    def __init__(
        self,
        name,
        width,
        depth,
        height,
        material="Concreto"
    ):

        super().__init__(
            name,
            "Column",
            material=material
        )

        self.width = width
        self.depth = depth
        self.height = height


        self.set_parameter(
            "Ancho",
            width
        )

        self.set_parameter(
            "Profundidad",
            depth
        )

        self.set_parameter(
            "Altura",
            height
        )