from models.structural.foundation import Foundation


class FoundationEngine:

    @staticmethod
    def create_isolated_foundation(
        point,
        width=2.00,
        length=2.00,
        thickness=0.60,
    ):
        return Foundation(
            insertion_point=point,
            foundation_type=Foundation.ISOLATED,
            width=width,
            length=length,
            thickness=thickness,
        )
