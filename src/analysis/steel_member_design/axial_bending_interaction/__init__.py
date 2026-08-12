class AxialBendingInteraction:
    def unity(self, axial, axial_capacity, mx, mx_capacity, my=0.0, my_capacity=1.0):
        return abs(axial)/axial_capacity + abs(mx)/mx_capacity + abs(my)/my_capacity
