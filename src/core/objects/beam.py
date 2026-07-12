from .element import Element


class Beam(Element):

    def __init__(
        self,
        name,
        length,
        section,
        material="Concreto"
    ):

        super().__init__(
            name,
            "Beam",
            material=material
        )

        self.length = length
        self.section = section


        self.set_parameter(
            "Longitud",
            length
        )

        self.set_parameter(
            "Seccion",
            section
        )