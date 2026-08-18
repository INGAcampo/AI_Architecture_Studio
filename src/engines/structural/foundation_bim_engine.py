class FoundationBimEngine:

    @staticmethod
    def update_properties(foundation):

        foundation.properties = {

            "Nivel": foundation.level,

            "Tipo": foundation.foundation_type,

            "Material": foundation.material,

            "Concreto": f"{foundation.concrete_strength_mpa} MPa",

            "Capacidad portante":
                f"{foundation.soil_bearing_capacity_kpa} kPa",

            "Profundidad":
                f"{foundation.foundation_depth_m} m",

            "Norma": foundation.design_code,

            "Sistema": foundation.unit_system,

        }

        return foundation.properties
