class StabilityDiagnostics:
    def messages(self, result, slenderness):
        out=['Stable.' if result.status=='PASS' else 'Unstable or overstressed.']
        if slenderness>200: out.append('Slenderness exceeds recommended limit.')
        return tuple(out)
