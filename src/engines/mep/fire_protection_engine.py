class FireProtectionEngine:

    @staticmethod
    def calculate_sprinklers(area_m2):

        coverage = 12.0

        return max(1, int(area_m2 / coverage))

    @staticmethod
    def hydraulic_demand(network):

        return 0.0
