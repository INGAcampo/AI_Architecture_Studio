from design.steel.compression_buckling import CompressionBucklingEngine

class BraceCompressionEngine:
    def __init__(self):
        self.buckling=CompressionBucklingEngine()

    def calculate(self, profile, material, slenderness):
        return self.buckling.calculate(profile,material,slenderness)
