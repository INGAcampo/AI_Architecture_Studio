class SteelMemberReport:
    def build(self, member, result, section_name):
        return (
            f"# Steel Member Design Report — {member.member_id}\n\n"
            f"- Section: {section_name}\n"
            f"- Maximum unity: {result.maximum_unity:.4f}\n"
            f"- Governing: {result.governing}\n"
            f"- Status: {result.status}\n"
        )
