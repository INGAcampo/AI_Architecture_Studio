class BeamAnalysis:

    @staticmethod
    def self_weight(beam):

        density = getattr(beam, "density_kg_m3", 2400.0)

        return beam.volume * density

    @staticmethod
    def distributed_load(beam):

        return getattr(beam, "distributed_load_kg_m", 0.0)

    @staticmethod
    def point_load(beam):

        return getattr(beam, "point_load_kg", 0.0)

    @staticmethod
    def maximum_shear(beam):

        L = getattr(beam, "length", 0.0)
        q = BeamAnalysis.distributed_load(beam)

        return (q * L) / 2.0

    @staticmethod
    def maximum_moment(beam):

        L = getattr(beam, "length", 0.0)
        q = BeamAnalysis.distributed_load(beam)

        return (q * L * L) / 8.0
