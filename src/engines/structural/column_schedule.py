class ColumnSchedule:

    @staticmethod
    def generate(columns):

        return [

            {

                "nombre": c.name,

                "nivel": c.level,

                "material": c.material,

            }

            for c in columns

        ]
