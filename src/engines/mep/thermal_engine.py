class ThermalEngine:

    @staticmethod
    def calculate_cooling_load(area_m2):

        watts_per_m2 = 120.0

        return area_m2 * watts_per_m2

    @staticmethod
    def calculate_heating_load(area_m2):

        watts_per_m2 = 80.0

        return area_m2 * watts_per_m2
