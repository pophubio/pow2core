from decimal import Decimal

from pow2core.factors.implementations.combination import CombinationFactorByValue


class TestCombinationFactorByValue:
    def test(self):
        factor = CombinationFactorByValue(precision=3)

        value1 = 2
        result1 = factor.get_weight(value1)
        assert result1.value == value1
        assert result1.weight == Decimal("2.000")

        value2 = Decimal("3.125")
        result2 = factor.get_weight(value2)
        assert result2.value == value2
        assert result2.weight == Decimal("3.125")
