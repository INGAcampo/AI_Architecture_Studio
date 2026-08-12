from models.structural.beam import Beam


class BeamEngine:

    @staticmethod
    def create_beam(
        start_point,
        end_point,
        width=0.25,
        height=0.50,
        elevation=3.00,
    ):
        return Beam(
            start_point=start_point,
            end_point=end_point,
            width=width,
            height=height,
            elevation=elevation,
        )
