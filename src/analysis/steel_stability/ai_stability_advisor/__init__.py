class AiStabilityAdvisor:
    def advise(self, result):
        if result.status=='FAIL': return 'Increase stiffness, reduce unbraced length, or add bracing.'
        if result.maximum_unity>0.90: return 'Stable with limited reserve.'
        return 'Stable with adequate reserve.'
