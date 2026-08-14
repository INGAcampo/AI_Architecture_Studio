from __future__ import annotations

from .contracts import BridgeMesh, BridgeTopologySummary


def require_occt():
    try:
        import OCP
    except Exception as exc:
        raise RuntimeError("OCP/OCCT runtime is not available") from exc
    return OCP


def topology_summary(shape) -> BridgeTopologySummary:
    require_occt()

    from OCP.TopAbs import (
        TopAbs_SOLID,
        TopAbs_SHELL,
        TopAbs_FACE,
        TopAbs_WIRE,
        TopAbs_EDGE,
        TopAbs_VERTEX,
    )
    from OCP.TopExp import TopExp_Explorer

    def count(kind) -> int:
        explorer = TopExp_Explorer(shape, kind)
        value = 0
        while explorer.More():
            value += 1
            explorer.Next()
        return value

    return BridgeTopologySummary(
        solids=count(TopAbs_SOLID),
        shells=count(TopAbs_SHELL),
        faces=count(TopAbs_FACE),
        wires=count(TopAbs_WIRE),
        edges=count(TopAbs_EDGE),
        vertices=count(TopAbs_VERTEX),
    )


def make_box(dx: float, dy: float, dz: float):
    require_occt()
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox

    if dx <= 0 or dy <= 0 or dz <= 0:
        raise ValueError("box dimensions must be positive")
    shape = BRepPrimAPI_MakeBox(float(dx), float(dy), float(dz)).Shape()
    if shape.IsNull():
        raise RuntimeError("OCCT returned a null box shape")
    return shape


def triangulate(shape, linear_deflection: float = 0.5) -> BridgeMesh:
    require_occt()

    if linear_deflection <= 0:
        raise ValueError("linear_deflection must be positive")

    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopLoc import TopLoc_Location
    from OCP.TopoDS import TopoDS

    mesher = BRepMesh_IncrementalMesh(shape, float(linear_deflection))
    mesher.Perform()

    vertices = []
    triangles = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)

    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        location = TopLoc_Location()
        triangulation = BRep_Tool.Triangulation_s(face, location)

        if triangulation is not None:
            transformation = location.Transformation()
            offset = len(vertices)

            for index in range(1, triangulation.NbNodes() + 1):
                point = triangulation.Node(index).Transformed(transformation)
                vertices.append((float(point.X()), float(point.Y()), float(point.Z())))

            for index in range(1, triangulation.NbTriangles() + 1):
                triangle = triangulation.Triangle(index)
                n1, n2, n3 = triangle.Get()
                if face.Orientation() != 0:
                    n2, n3 = n3, n2
                triangles.append((offset + n1 - 1, offset + n2 - 1, offset + n3 - 1))

        explorer.Next()

    mesh = BridgeMesh(tuple(vertices), tuple(triangles))
    mesh.validate()
    return mesh
