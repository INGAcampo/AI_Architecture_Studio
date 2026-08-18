class BiaxialBendingEngine:
    def unity(self, mx, mpx, my, mpy):
        return abs(mx)/mpx + abs(my)/mpy
