class LocalBucklingClassifier:
    def classify(self, slenderness, compact_limit, noncompact_limit):
        if slenderness <= compact_limit: return "compact"
        if slenderness <= noncompact_limit: return "noncompact"
        return "slender"
