from __future__ import annotations

from dataclasses import dataclass

from .model import Opening


@dataclass(frozen=True, slots=True)
class OpeningCollision:
    first_id: str
    second_id: str
    overlap: float


class OpeningCollisionDetector:
    def detect(self, openings: tuple[Opening, ...]) -> tuple[OpeningCollision, ...]:
        ordered = sorted(openings, key=lambda item: item.placement.offset)
        collisions: list[OpeningCollision] = []

        for index, first in enumerate(ordered):
            first_start = first.placement.offset
            first_end = first_start + first.width
            first_bottom = first.placement.sill_height
            first_top = first.head_height

            for second in ordered[index + 1:]:
                second_start = second.placement.offset
                if second_start >= first_end:
                    break
                second_end = second_start + second.width
                second_bottom = second.placement.sill_height
                second_top = second.head_height

                horizontal_overlap = min(first_end, second_end) - max(first_start, second_start)
                vertical_overlap = min(first_top, second_top) - max(first_bottom, second_bottom)
                if horizontal_overlap > 0 and vertical_overlap > 0:
                    collisions.append(
                        OpeningCollision(
                            first.opening_id,
                            second.opening_id,
                            horizontal_overlap * vertical_overlap,
                        )
                    )

        return tuple(collisions)
