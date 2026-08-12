class SectionReportEngine:
    def build(self,m,s): return f"# Steel Library Report — {s.designation}\n\n- Material: {m.name}\n- Fy: {m.fy_mpa:.1f} MPa\n- Area: {s.area_mm2:.1f} mm²\n- Mass: {s.mass_kg_m:.2f} kg/m\n"
