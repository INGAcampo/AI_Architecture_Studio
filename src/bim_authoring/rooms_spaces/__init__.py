from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Room:
    room_id: str
    name: str
    boundary: tuple[tuple[float,float], ...]
    height: float
    level_id: str

@dataclass(frozen=True, slots=True)
class Space:
    space_id: str
    room_id: str
    discipline: str
    occupancy: int

@dataclass(frozen=True, slots=True)
class RoomQuantities:
    area: float
    perimeter: float
    volume: float

class NativeBimRoomSpaceEngine:
    def area(self, points):
        return abs(sum(
            points[i][0]*points[(i+1)%len(points)][1] -
            points[(i+1)%len(points)][0]*points[i][1]
            for i in range(len(points))
        )) / 2

    def perimeter(self, points):
        from math import hypot
        return sum(
            hypot(
                points[(i+1)%len(points)][0]-points[i][0],
                points[(i+1)%len(points)][1]-points[i][1],
            )
            for i in range(len(points))
        )

    def quantities(self, room):
        area = self.area(room.boundary)
        perimeter = self.perimeter(room.boundary)
        return RoomQuantities(area, perimeter, area*room.height)

    def occupancy_density(self, room, space):
        return space.occupancy / self.quantities(room).area
