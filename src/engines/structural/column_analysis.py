class ColumnAnalysis:

    @staticmethod
    def self_weight(column):

        density = getattr(column, "density_kg_m3", 2400.0)

        return column.volume * density

    @staticmethod
    def axial_load(column):

        self_weight = ColumnAnalysis.self_weight(column)

        slab_load = getattr(column, "supported_slab_load_kg", 0.0)

        beam_load = getattr(column, "supported_beam_load_kg", 0.0)

        return self_weight + slab_load + beam_load

    @staticmethod
    def service_load(column):

        live_load = getattr(column, "supported_live_load_kg", 0.0)

        return ColumnAnalysis.axial_load(column) + live_load
