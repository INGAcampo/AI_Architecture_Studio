class BeamBimEngine:

    @staticmethod
    def update_properties(beam):

        beam.properties = {

            "Nivel": beam.level,

            "Tipo": beam.beam_type,

            "Material": beam.material,

            "Concreto": f"{beam.concrete_strength_mpa} MPa",

            "Acero": beam.steel_grade,

            "Perfil": beam.profile,

            "Recubrimiento": f"{beam.cover_cm} cm",

            "Norma": beam.design_code,

            "Sistema": beam.unit_system,

        }

        return beam.properties
