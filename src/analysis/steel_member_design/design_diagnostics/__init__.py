class DesignDiagnostics:
    def messages(self, result):
        out=[]
        if result.maximum_unity > 1.0: out.append("Member does not comply.")
        elif result.maximum_unity > 0.90: out.append("Member is near capacity.")
        else: out.append("Member has adequate reserve.")
        return tuple(out)
