class SlendernessEngine:
    def ratio(self, k, length_mm, radius_mm):
        return k*length_mm/max(radius_mm,1e-12)
    def acceptable(self, ratio, limit=200.0):
        return ratio <= limit
