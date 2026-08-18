class EnergyAnalysisEngine:

    @staticmethod
    def calculate_consumption(area_m2):

        return area_m2 * 45.0

    @staticmethod
    def estimate_savings(consumption_kwh):

        return consumption_kwh * 0.20
