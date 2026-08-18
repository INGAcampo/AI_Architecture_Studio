class BarSelectionEngine:
    def select(self,required_area,bar_areas):
        c=[(n,a) for a in bar_areas for n in range(2,13) if n*a>=required_area]
        return min(c,key=lambda x:x[0]*x[1]) if c else None
