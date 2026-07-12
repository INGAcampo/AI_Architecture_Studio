from .element import Element


class Wall(Element):

    def __init__(
        self,
        name,
        length,
        height,
        thickness,
        material="Concreto"
    ):

        super().__init__(
            name,
            "Wall",
            material=material
        )

        self.length = length
        self.height = height
        self.thickness = thickness


        self.set_parameter(
            "Longitud",
            length
        )

        self.set_parameter(
            "Altura",
            height
        )

        self.set_parameter(
            "Espesor",
            thickness
        )