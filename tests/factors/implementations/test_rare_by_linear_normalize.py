from decimal import Decimal

from pow2core.factors.implementations.rare import RareFactorByLinearNormalize


class TestRareFactorByLinearNormalize:
    def test_gcw(self):
        factor = RareFactorByLinearNormalize(
            min_rare=1,
            max_rare=9432,
            alpha=1047,
            precision=2,
        )

        assert factor.get_weight(1).weight == Decimal("10.00")
        assert factor.get_weight(2339).weight == Decimal("7.77")
        assert factor.get_weight(9432).weight == Decimal("1.00")
