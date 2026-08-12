"""Pruebas geométricas para ROOM 5.0.7.3."""

from engines.architectural.room_graph import RoomGraph
from engines.geometry.point import Point


def test_square_face():
    graph = RoomGraph()
    a = Point(0, 0, 0)
    b = Point(4, 0, 0)
    c = Point(4, 3, 0)
    d = Point(0, 3, 0)

    graph.add_edge(a, b)
    graph.add_edge(b, c)
    graph.add_edge(c, d)
    graph.add_edge(d, a)

    faces = graph.faces()
    assert len(faces) == 1
    assert abs(RoomGraph.signed_area(faces[0]) - 12.0) < 1.0e-6


def test_two_rooms():
    graph = RoomGraph()
    points = [
        Point(0, 0, 0),
        Point(4, 0, 0),
        Point(8, 0, 0),
        Point(8, 3, 0),
        Point(4, 3, 0),
        Point(0, 3, 0),
    ]
    a, b, c, d, e, f = points

    for first, second in (
        (a, b), (b, c), (c, d), (d, e),
        (e, f), (f, a), (b, e),
    ):
        graph.add_edge(first, second)

    faces = graph.faces()
    areas = sorted(round(RoomGraph.signed_area(face), 6) for face in faces)
    assert areas == [12.0, 12.0]


if __name__ == "__main__":
    test_square_face()
    test_two_rooms()
    print("ROOM AUTODETECT: OK")
