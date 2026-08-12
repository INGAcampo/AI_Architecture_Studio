"""Cuadro de áreas de ROOM."""


class RoomSchedule:
    @staticmethod
    def rows(scene):
        getter = getattr(scene, "get_elements", None)
        elements = getter() if callable(getter) else []
        rooms = [
            item for item in elements
            if item.__class__.__name__ == "Room"
            and getattr(item, "valid", False)
        ]
        rooms.sort(
            key=lambda room: (
                str(getattr(room, "number", "")),
                str(getattr(room, "name", "")),
            )
        )
        return [
            {
                "number": getattr(room, "number", ""),
                "name": getattr(room, "name", "Ambiente"),
                "category": getattr(room, "category_label", "General"),
                "area": float(getattr(room, "area", 0.0)),
                "perimeter": float(getattr(room, "perimeter", 0.0)),
            }
            for room in rooms
        ]

    @classmethod
    def totals(cls, scene):
        rows = cls.rows(scene)
        return {
            "count": len(rows),
            "area": sum(row["area"] for row in rows),
            "perimeter": sum(row["perimeter"] for row in rows),
        }

    @classmethod
    def console_report(cls, scene):
        rows = cls.rows(scene)
        totals = cls.totals(scene)
        lines = [
            "ROOM SCHEDULE 5.0.7.4",
            "-" * 74,
            f"{'Nº':<8}{'Nombre':<24}{'Categoría':<20}{'Área m²':>10}",
            "-" * 74,
        ]
        for row in rows:
            lines.append(
                f"{row['number'] or '-':<8}"
                f"{row['name'][:22]:<24}"
                f"{row['category'][:18]:<20}"
                f"{row['area']:>10.2f}"
            )
        lines.extend(
            [
                "-" * 74,
                f"Ambientes: {totals['count']}",
                f"Área útil total: {totals['area']:.2f} m²",
            ]
        )
        return "\n".join(lines)
