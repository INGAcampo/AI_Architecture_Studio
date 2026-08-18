from design.steel.column_domain import ColumnEndCondition, EffectiveLength

class EffectiveLengthEngine:
    DEFAULT_K = {
        ColumnEndCondition.PINNED_PINNED: 1.0,
        ColumnEndCondition.FIXED_FIXED: 0.65,
        ColumnEndCondition.FIXED_PINNED: 0.80,
        ColumnEndCondition.FIXED_FREE: 2.0,
    }

    def factor(self, condition, custom=None):
        if condition is ColumnEndCondition.CUSTOM:
            if custom is None or custom <= 0:
                raise ValueError("Factor K personalizado inválido")
            return float(custom)
        return self.DEFAULT_K[condition]

    def effective_length(self, length, condition, custom=None):
        if length <= 0:
            raise ValueError("Longitud inválida")
        return EffectiveLength(length, self.factor(condition, custom))
