class ElectricalEngine:

    @staticmethod
    def calculate_total_load(panel):

        return sum(
            circuit.power_w
            for circuit in panel.circuits
        )

    @staticmethod
    def calculate_current(power_w, voltage_v):

        if voltage_v <= 0:
            return 0.0

        return power_w / voltage_v
