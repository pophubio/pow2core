from decimal import Decimal

from pow2core.factors.implementations.rare import RareFactorByFixed


class TestRareFactorByFixed:
    def test_init_with_int_weights(self):
        weights = {1: 10, 2: 20, 3: 30}
        factor = RareFactorByFixed(weights)

        assert factor.name == "rare"
        assert factor.weights == weights
        assert factor.precision == 2

    def test_init_with_decimal_weights(self):
        weights = {Decimal('1.5'): Decimal('10.5'), Decimal('2.5'): Decimal('20.5')}
        factor = RareFactorByFixed(weights, precision=3)

        assert factor.name == "rare"
        assert factor.weights == weights
        assert factor.precision == 3

    def test_init_with_mixed_weights(self):
        weights = {1: 10, 2: 20, 3: 30, Decimal('1.5'): Decimal('10.5'), Decimal('2.5'): Decimal('20.5')}
        factor = RareFactorByFixed(weights, precision=3)

        assert factor.name == "rare"
        assert factor.weights == weights
        assert factor.precision == 3

    def test_get_weight_with_int_value(self):
        weights = {1: 10, 2: 20, 3: 30}
        factor = RareFactorByFixed(weights)
        assert factor.get_weight(1).weight == Decimal('10.00')
        assert factor.get_weight(2).weight == Decimal('20.00')
        assert factor.get_weight(3).weight == Decimal('30.00')

    def test_get_weight_with_decimal_value(self):
        weights = {Decimal('1.5'): Decimal('10.5'), Decimal('2.5'): Decimal('20.5')}
        factor = RareFactorByFixed(weights, precision=3)
        assert factor.get_weight(Decimal('1.5')).weight == Decimal('10.500')
        assert factor.get_weight(Decimal('2.5')).weight == Decimal('20.500')
