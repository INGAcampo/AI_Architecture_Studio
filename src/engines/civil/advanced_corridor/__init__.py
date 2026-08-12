from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CorridorStation:
    station: float
    elevation: float
    width: float

class AdvancedCorridorEngine:
    def interpolate(self, a, b, station):
        if not a.station <= station <= b.station:
            raise ValueError("Station fuera del tramo")
        ratio = (station-a.station)/(b.station-a.station)
        return CorridorStation(
            station,
            a.elevation + ratio*(b.elevation-a.elevation),
            a.width + ratio*(b.width-a.width),
        )

    def corridor_length(self, stations):
        stations = tuple(stations)
        return stations[-1].station - stations[0].station
