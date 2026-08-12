class FoundationAnalysis:

    @staticmethod
    def self_weight(foundation):

        density = getattr(
            foundation,
            "density_kg_m3",
            2400.0,
        )

        return foundation.volume * density

    @staticmethod
    def column_load(foundation):

        return getattr(
            foundation,
            "supported_column_load_kg",
            0.0,
        )

    @staticmethod
    def service_load(foundation):

        return (
            FoundationAnalysis.self_weight(foundation)
            + FoundationAnalysis.column_load(foundation)
        )

    @staticmethod
    def soil_pressure(foundation):

        area = getattr(
            foundation,
            "area",
            1.0,
        )

        if area <= 0:
            return 0.0

        return (
            FoundationAnalysis.service_load(foundation)
            / area
        )

    @staticmethod
    def check_bearing_capacity(foundation):

        pressure = FoundationAnalysis.soil_pressure(
            foundation
        )

        capacity = getattr(
            foundation,
            "soil_bearing_capacity_kpa",
            150.0,
        )

        return pressure <= capacity
