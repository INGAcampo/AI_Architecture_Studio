from dataclasses import replace

class SheetManager:
    def __init__(self):
        self._sheets = {}

    def add(self, sheet, *, replace_existing=False):
        if sheet.sheet_id in self._sheets and not replace_existing:
            raise ValueError(f"Hoja duplicada: {sheet.sheet_id}")
        self._sheets[sheet.sheet_id] = sheet

    def get(self, sheet_id):
        return self._sheets[sheet_id]

    def place_viewport(self, sheet_id, viewport):
        sheet = self._sheets[sheet_id]
        for existing in sheet.viewports:
            if self._overlap(existing, viewport):
                raise ValueError("El viewport se superpone con otro")
        updated = replace(sheet, viewports=sheet.viewports + (viewport,))
        self._sheets[sheet_id] = updated
        return updated

    def _overlap(self, a, b):
        return not (
            a.x + a.width <= b.x
            or b.x + b.width <= a.x
            or a.y + a.height <= b.y
            or b.y + b.height <= a.y
        )

    def all(self):
        return tuple(self._sheets[key] for key in sorted(self._sheets))
