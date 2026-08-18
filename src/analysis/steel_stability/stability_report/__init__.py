class StabilityReport:
    def build(self, member_id, result, slenderness):
        return f"# Steel Stability Report — {member_id}\n\n- Slenderness: {slenderness:.3f}\n- Maximum unity: {result.maximum_unity:.4f}\n- Governing: {result.governing}\n- Status: {result.status}\n"
