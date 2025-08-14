import pytest
from decimal import Decimal

from pow2core.factors.algorithms.fixed import FactorByFixed


class TestFactorByFixed:
    def test_init_with_int_weights(self):
        weights = {1: 10, 2: 20, 3: 30}
        factor = FactorByFixed("test_factor", weights, max_weight=30, is_visible=True)

        assert factor.name == "test_factor"
        assert factor.weights == weights
        assert factor.precision == 2

    def test_init_with_decimal_weights(self):
        weights = {Decimal('1.5'): Decimal('10.5'), Decimal('2.5'): Decimal('20.5')}
        factor = FactorByFixed("test_factor", weights, precision=3, max_weight=20.5, is_visible=True)

        assert factor.name == "test_factor"
        assert factor.weights == weights
        assert factor.precision == 3

    def test_init_with_mixed_weights(self):
        weights = {1: Decimal('10.5'), Decimal('2.5'): 20}
        factor = FactorByFixed("test_factor", weights, precision=3, max_weight=20.5, is_visible=True)

        assert factor.name == "test_factor"
        assert factor.weights == weights

    def test_get_weight_with_int_value(self):
        weights = {1: 10, 2: 20, 3: 30}
        factor = FactorByFixed("test_factor", weights, max_weight=30, is_visible=True)

        result = factor.get_weight(1)
        assert result.value == 1
        assert result.weight == Decimal('10.00')

    def test_get_weight_with_decimal_value(self):
        weights = {Decimal('1.5'): Decimal('10.5')}
        factor = FactorByFixed("test_factor", weights, max_weight=20.5, is_visible=True)

        result = factor.get_weight(Decimal('1.5'))
        assert result.value == Decimal('1.5')
        assert result.weight == Decimal('10.50')

    def test_get_weight_precision_control(self):
        weights = {1: Decimal('10.123456')}
        factor = FactorByFixed("test_factor", weights, precision=4, max_weight=15, is_visible=True)

        result = factor.get_weight(1)
        assert result.value == 1
        assert result.weight == Decimal('10.1235')

    def test_get_weight_value_not_found(self):
        weights = {1: 10, 2: 20}
        factor = FactorByFixed("test_factor", weights)

        with pytest.raises(ValueError, match="Value 3 not in weight keys"):
            factor.get_weight(3)

    def test_get_weight_invalid_value_type(self):
        weights = {1: 10}
        factor = FactorByFixed("test_factor", weights)

        with pytest.raises(ValueError, match="Value must be number"):
            factor.get_weight("invalid")

    def test_quantize_method_inheritance(self):
        weights = {1: 10}
        factor = FactorByFixed("test_factor", weights, precision=3)

        quantized = factor._quantize(Decimal('1.23456'))
        assert quantized == Decimal('1.235')

    def test_empty_weights_dict(self):
        weights = {}

        with pytest.raises(ValueError, match="Weights must be provided"):
            FactorByFixed("test_factor", weights)

    def test_zero_precision(self):
        weights = {1: Decimal('10.789')}
        factor = FactorByFixed("test_factor", weights, precision=0, max_weight=11, is_visible=True)

        result = factor.get_weight(1)
        assert result.value == 1
        assert result.weight == Decimal('11')

    def test_large_decimal_values(self):
        weights = {Decimal('999999999999.999'): Decimal('888888888888.888')}
        factor = FactorByFixed("test_factor", weights, precision=3, max_weight=1000000000000, is_visible=True)

        result = factor.get_weight(Decimal('999999999999.999'))
        assert result.value == Decimal('999999999999.999')
        assert result.weight == Decimal('888888888888.888')
