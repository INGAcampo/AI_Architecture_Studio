class ResultsEngine:

    @staticmethod
    def beam_forces(element):

        return {

            "shear": [],

            "moment": [],

        }

    @staticmethod
    def displacements(node):

        return {

            "ux": 0.0,

            "uy": 0.0,

            "uz": 0.0,

        }
