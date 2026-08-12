class AiDesignAdvisor:
    def advise(self, result):
        if result.status=="FAIL": return "Increase section capacity or reduce demand."
        if result.maximum_unity>0.90: return "Member passes with limited reserve."
        return "Member passes with adequate reserve."
