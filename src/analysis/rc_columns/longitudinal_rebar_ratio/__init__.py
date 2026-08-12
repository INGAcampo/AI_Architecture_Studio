class LongitudinalRebarRatioEngine:
    def ratio(self,steel_area,gross_area): return steel_area/max(gross_area,1e-12)
    def acceptable(self,ratio,minimum=.01,maximum=.08): return minimum<=ratio<=maximum
