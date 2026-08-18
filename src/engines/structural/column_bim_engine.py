class ColumnBimEngine:

    @staticmethod
    def update_properties(column):

        column.properties = {

            "Nivel": column.level,

            "Material": column.material,

            "Concreto": f"{column.concrete_strength_mpa} MPa",

            "Acero": column.steel_grade,

            "Recubrimiento": f"{column.cover_cm} cm",

            "Norma": column.design_code,

            "Sistema": column.unit_system,

        }

        return column.properties
