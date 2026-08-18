class ColumnEngine:

    @staticmethod
    def create_rectangular(point, width=0.30, depth=0.30, height=3.00):
        from models.structural.column import Column

        return Column(
            insertion_point=point,
            shape=Column.RECTANGULAR,
            width=width,
            depth=depth,
            height=height,
        )

    @staticmethod
    def create_circular(point, diameter=0.30, height=3.00):
        from models.structural.column import Column

        return Column(
            insertion_point=point,
            shape=Column.CIRCULAR,
            diameter=diameter,
            height=height,
        )
