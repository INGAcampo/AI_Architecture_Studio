class FoundationSchedule:

    @staticmethod
    def generate(foundations):

        return [

            {

                "nombre": f.name,

                "tipo": f.foundation_type,

                "nivel": f.level,

                "material": f.material,

            }

            for f in foundations

        ]
