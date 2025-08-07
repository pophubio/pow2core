import pytest
from decimal import Decimal

from pow2core.factors.algorithms.linear import FactorByLinear


class TestFactorByLinear:
    def test_init_with_default_weights(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        assert factor.name == "test_factor"
        assert factor.min_value == 10
        assert factor.max_value == 100
        assert factor.min_weight == Decimal("1.00")
        assert factor.max_weight == Decimal("5.00")

    def test_init_with_custom_weights(self):
        factor = FactorByLinear(
            "test_factor",
            min_value=5,
            max_value=50,
            min_weight=Decimal("2.5"),
            max_weight=Decimal("10.0")
        )

        assert factor.min_value == 5
        assert factor.max_value == 50
        assert factor.min_weight == Decimal("2.5")
        assert factor.max_weight == Decimal("10.0")

    def test_get_weight_below_min_value(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(5)
        assert result.value == 5
        assert result.weight == Decimal("1.00")

    def test_get_weight_at_min_value(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(10)
        assert result.value == 10
        assert result.weight == Decimal("1.00")

    def test_get_weight_above_max_value(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(150)
        assert result.value == 150
        assert result.weight == Decimal("5.00")

    def test_get_weight_at_max_value(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(100)
        assert result.value == 100
        assert result.weight == Decimal("5.00")

    def test_get_weight_midpoint(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(55)  # Midpoint
        assert result.value == 55
        assert result.weight == Decimal("3.00")

    def test_get_weight_linear_calculation(self):
        factor = FactorByLinear(
            "test_factor",
            min_value=0,
            max_value=100,
            min_weight=Decimal("0"),
            max_weight=Decimal("10")
        )

        result = factor.get_weight(25)
        assert result.value == 25
        assert result.weight == Decimal("2.50")

        result = factor.get_weight(75)
        assert result.value == 75
        assert result.weight == Decimal("7.50")

    def test_get_weight_with_decimal_input(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(Decimal("55.5"))
        expected = Decimal("1.00") + (Decimal("5.00") - Decimal("1.00")) / (100 - 10) * (Decimal("55.5") - 10)
        assert result.value == 55.5
        assert result.weight == expected.quantize(Decimal("0.01"))

    def test_get_weight_with_float_input(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        result = factor.get_weight(55.5)
        expected = Decimal("1.00") + (Decimal("5.00") - Decimal("1.00")) / (100 - 10) * (Decimal("55.5") - 10)
        assert result.value == 55.5
        assert result.weight == expected.quantize(Decimal("0.01"))

    def test_get_weight_invalid_value_type(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        with pytest.raises(ValueError, match="Value must be number"):
            factor.get_weight("invalid")

    def test_get_weight_with_none(self):
        factor = FactorByLinear("test_factor", min_value=10, max_value=100)

        with pytest.raises(ValueError, match="Value must be number"):
            factor.get_weight(None)

    def test_precision_control(self):
        factor = FactorByLinear(
            "test_factor",
            min_value=0,
            max_value=3,
            min_weight=Decimal("0"),
            max_weight=Decimal("1")
        )

        result = factor.get_weight(1)
        # Should be 1/3 = 0.33333... quantized to 2 decimal places
        assert result.value == 1
        assert result.weight == Decimal("0.33")

    def test_negative_values(self):
        factor = FactorByLinear(
            "test_factor",
            min_value=-10,
            max_value=10,
            min_weight=Decimal("0"),
            max_weight=Decimal("20")
        )

        assert factor.get_weight(-15).weight == Decimal("0")
        assert factor.get_weight(-10).weight == Decimal("0")
        assert factor.get_weight(0).weight == Decimal("10.00")
        assert factor.get_weight(10).weight == Decimal("20")
        assert factor.get_weight(15).weight == Decimal("20")

    def test_same_min_max_values(self):
        factor = FactorByLinear(
            "test_factor",
            min_value=50,
            max_value=50,
            min_weight=Decimal("2"),
            max_weight=Decimal("8")
        )

        # When min_value == max_value, division by zero should be handled
        # Values <= min_value should return min_weight
        # Values >= max_value should return max_weight
        assert factor.get_weight(25).weight == Decimal("2")  # Below range
        assert factor.get_weight(50).weight == Decimal("2")  # At min_value (also max_value)
        assert factor.get_weight(75).weight == Decimal("8")  # Above range

    def test_inverted_weight_range(self):
        # Test where min_weight > max_weight (decreasing function)
        factor = FactorByLinear(
            "test_factor",
            min_value=10,
            max_value=100,
            min_weight=Decimal("10"),
            max_weight=Decimal("1")
        )

        result = factor.get_weight(55)  # Midpoint
        assert result.value == 55
        assert result.weight == Decimal("5.50")

    def test_large_numbers(self):
        factor = FactorByLinear(
            "test_factor",
            min_value=1000000,
            max_value=2000000,
            min_weight=Decimal("100"),
            max_weight=Decimal("200")
        )

        result = factor.get_weight(1500000)  # Midpoint
        assert result.value == 1500000
        assert result.weight == Decimal("150.00")
