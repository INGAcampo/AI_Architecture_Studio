from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EarthworkZone:
    zone_id: str
    cut: float
    fill: float

class EarthworkBalancingEngine:
    def totals(self, zones):
        return (
            sum(z.cut for z in zones),
            sum(z.fill for z in zones),
        )

    def balance(self, zones):
        cut, fill = self.totals(zones)
        return fill-cut
