class LoadCaseEngine:

    DEFAULT_CASES = [

        ("Carga Muerta", "dead", 1.0),

        ("Carga Viva", "live", 1.0),

        ("Viento", "wind", 1.0),

        ("Sismo", "seismic", 1.0),
    ]

    @staticmethod
    def generate_defaults():

        return LoadCaseEngine.DEFAULT_CASES
