from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LayoutItem:
    item_id: str
    x: float
    y: float
    width: float
    height: float

class LayoutViewportManager:
    def fit(self, item, sheet_width, sheet_height, margin=10):
        scale = min(
            (sheet_width - 2 * margin) / item.width,
            (sheet_height - 2 * margin) / item.height,
        )
        return scale

    def arrange_grid(self, items, columns, gap=10):
        arranged = []
        for index, item in enumerate(items):
            col = index % columns
            row = index // columns
            arranged.append(
                LayoutItem(
                    item.item_id,
                    col * (item.width + gap),
                    row * (item.height + gap),
                    item.width,
                    item.height,
                )
            )
        return tuple(arranged)
