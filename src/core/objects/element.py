"""
AIAS Element Base Class

Objeto base para todos los elementos
arquitectónicos, estructurales y BIM.
"""


class Element:

    def __init__(
        self,
        name,
        element_type,
        level=None,
        material=None
    ):

        self.name = name
        self.element_type = element_type
        self.level = level
        self.material = material

        # Propiedades BIM
        self.parameters = {}

        # Geometría futura
        self.geometry = None


    def set_parameter(self, key, value):

        self.parameters[key] = value


    def get_parameter(self, key):

        return self.parameters.get(key)


    def info(self):

        return {
            "Nombre": self.name,
            "Tipo": self.element_type,
            "Nivel": self.level,
            "Material": self.material,
            "Parametros": self.parameters
        }