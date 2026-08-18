class BeamSchedule:

    @staticmethod
    def generate(beams):

        return [

            {

                "nombre": beam.name,

                "nivel": beam.level,

                "perfil": beam.profile,

                "material": beam.material,

            }

            for beam in beams

        ]
