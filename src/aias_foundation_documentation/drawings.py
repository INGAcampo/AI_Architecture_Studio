"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

from html import escape
from pathlib import Path

from aias_foundation_objects.models import FoundationObject

from .models import BarMark


class FoundationSvgWriter:
    """Execute the public FoundationSvgWriter operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    def write_plan(self, foundation: FoundationObject, bars: list[BarMark], path: Path) -> Path:
        """Persist plan for foundation drawings, schedules and technical documentation in its stable external representation."""
        path.parent.mkdir(parents=True, exist_ok=True)
        g = foundation.geometry
        scale = min(520 / g.length_m, 360 / g.width_m)
        w, h = g.length_m * scale, g.width_m * scale
        x, y = (760 - w) / 2, 110
        support = foundation.supports[0]
        sw, sh = support.width_m * scale, support.depth_m * scale
        sx, sy = x + w / 2 - sw / 2, y + h / 2 - sh / 2
        lines = []
        for bar in bars:
            lines.append(f'<text x="80" y="{530 + len(lines)*24}" class="note">{escape(bar.mark)}: Ø{bar.diameter_mm} @ {bar.spacing_mm} mm - {escape(bar.direction)}</text>')
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="640" viewBox="0 0 760 640">
<style>.outline{{fill:none;stroke:#111827;stroke-width:4}}.bar{{stroke:#2563eb;stroke-width:2}}.dim{{stroke:#64748b;stroke-width:1}}.title{{font:700 24px sans-serif}}.note{{font:16px sans-serif}}</style>
<rect width="760" height="640" fill="white"/><text x="40" y="45" class="title">AIAS FOUNDATION PLAN - {escape(foundation.name)}</text>
<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" class="outline"/><rect x="{sx:.2f}" y="{sy:.2f}" width="{sw:.2f}" height="{sh:.2f}" fill="#cbd5e1" stroke="#111827" stroke-width="3"/>
<line x1="{x:.2f}" y1="{y+h/2:.2f}" x2="{x+w:.2f}" y2="{y+h/2:.2f}" class="bar"/><line x1="{x+w/2:.2f}" y1="{y:.2f}" x2="{x+w/2:.2f}" y2="{y+h:.2f}" class="bar"/>
<text x="{x+w/2-35:.2f}" y="{y-20:.2f}" class="note">L={g.length_m:.3f} m</text><text x="{x+w+15:.2f}" y="{y+h/2:.2f}" class="note">B={g.width_m:.3f} m</text>
{''.join(lines)}<text x="40" y="615" class="note">REFERENCE_ONLY - Professional review required</text></svg>'''
        path.write_text(svg, encoding="utf-8")
        return path

    def write_section(self, foundation: FoundationObject, bars: list[BarMark], path: Path) -> Path:
        """Persist section for foundation drawings, schedules and technical documentation in its stable external representation."""
        path.parent.mkdir(parents=True, exist_ok=True)
        g = foundation.geometry
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="480" viewBox="0 0 760 480">
<style>.o{{fill:#e5e7eb;stroke:#111827;stroke-width:4}}.b{{stroke:#2563eb;stroke-width:5}}.t{{font:16px sans-serif}}.h{{font:700 24px sans-serif}}</style><rect width="760" height="480" fill="white"/>
<text x="40" y="45" class="h">AIAS FOUNDATION SECTION - {escape(foundation.name)}</text><rect x="100" y="140" width="560" height="180" class="o"/>
<line x1="125" y1="{320-foundation.cover_m*180:.2f}" x2="635" y2="{320-foundation.cover_m*180:.2f}" class="b"/>
<rect x="315" y="80" width="130" height="160" class="o"/><text x="680" y="235" class="t">h={g.thickness_m:.3f} m</text>
<text x="100" y="360" class="t">Cover={foundation.cover_m*1000:.0f} mm | Bottom steel: {escape(', '.join(f'{b.mark} Ø{b.diameter_mm}@{b.spacing_mm}' for b in bars))}</text>
<text x="40" y="445" class="t">REFERENCE_ONLY - Not for construction without verified code pack and professional approval</text></svg>'''
        path.write_text(svg, encoding="utf-8")
        return path
