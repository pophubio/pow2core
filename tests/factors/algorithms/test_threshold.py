import pytest
from decimal import Decimal

from pow2core.factors.algorithms.threshold import FactorByThreshold


class TestFactorByThreshold:
    def test_init_with_matching_lengths(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        assert factor.name == "test_factor"
        assert factor.thresholds == [100, 50, 10]  # Should be sorted in descending order
        assert factor.weights == weights
        assert factor.precision == 2

    def test_init_mismatched_lengths(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0]  # Missing one weight

        with pytest.raises(ValueError, match="Thresholds and weights must have the same length"):
            FactorByThreshold("test_factor", thresholds, weights)

    def test_init_empty_lists(self):
        with pytest.raises(ValueError, match="Thresholds and weights must have the same length"):
            FactorByThreshold("test_factor", [], [1.0])

    def test_thresholds_sorted_descending(self):
        thresholds = [10, 100, 50]  # Unsorted input
        weights = [1.0, 5.0, 3.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        # Thresholds should be sorted in descending order
        assert factor.thresholds == [100, 50, 10]
        # Weights should remain in original order
        assert factor.weights == [1.0, 5.0, 3.0]

    def test_get_weight_above_highest_threshold(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(150)
        assert result.value == 150
        assert result.weight == Decimal('5.0')

    def test_get_weight_at_threshold(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(100)
        assert result.value == 100
        assert result.weight == Decimal('5.0')

        result = factor.get_weight(50)
        assert result.value == 50
        assert result.weight == Decimal('3.0')  # Should match highest threshold >= value

        result = factor.get_weight(10)
        assert result.value == 10
        assert result.weight == Decimal('1.0')  # Should match highest threshold >= value

    def test_get_weight_between_thresholds(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(75)  # Between 100 and 50
        assert result.value == 75
        assert result.weight == Decimal('3.0')

        result = factor.get_weight(25)  # Between 50 and 10
        assert result.value == 25
        assert result.weight == Decimal('1.0')

    def test_get_weight_below_lowest_threshold(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        with pytest.raises(ValueError, match="Value 5 less than min threshold 10"):
            factor.get_weight(5)

    def test_get_weight_with_decimal_input(self):
        thresholds = [100.5, 50.5, 10.5]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(Decimal('75.3'))
        assert result.value == Decimal('75.3')
        assert result.weight == Decimal('3.0')

    def test_get_weight_with_float_input(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(75.5)
        assert result.value == 75.5
        assert result.weight == Decimal('3.0')

    def test_get_weight_invalid_value_type(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        with pytest.raises(ValueError, match="Value must be number"):
            factor.get_weight("invalid")

    def test_get_weight_with_none(self):
        thresholds = [100, 50, 10]
        weights = [5.0, 3.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        with pytest.raises(ValueError, match="Value must be number"):
            factor.get_weight(None)

    def test_with_decimal_thresholds_and_weights(self):
        thresholds = [Decimal('100'), Decimal('50'), Decimal('10')]
        weights = [Decimal('5.5'), Decimal('3.3'), Decimal('1.1')]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(75)
        assert result.value == 75
        assert result.weight == Decimal('3.30')  # Should be quantized to 2 decimal places

    def test_single_threshold(self):
        thresholds = [50]
        weights = [3.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        assert factor.get_weight(100).weight == Decimal('3.0')
        assert factor.get_weight(50).weight == Decimal('3.0')

        with pytest.raises(ValueError, match="Value 25 less than min threshold 50"):
            factor.get_weight(25)

    def test_negative_thresholds(self):
        thresholds = [10, 0, -10]
        weights = [3.0, 2.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        assert factor.get_weight(15).weight == Decimal('3.0')
        assert factor.get_weight(5).weight == Decimal('2.0')
        assert factor.get_weight(-5).weight == Decimal('1.0')

        with pytest.raises(ValueError, match="Value -15 less than min threshold -10"):
            factor.get_weight(-15)

    def test_zero_threshold(self):
        thresholds = [10, 0]
        weights = [2.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        assert factor.get_weight(5).weight == Decimal('1.0')
        assert factor.get_weight(0).weight == Decimal('1.0')

    def test_large_numbers(self):
        thresholds = [1000000, 500000, 100000]
        weights = [10.0, 5.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        assert factor.get_weight(2000000).weight == Decimal('10.0')
        assert factor.get_weight(750000).weight == Decimal('5.0')
        assert factor.get_weight(250000).weight == Decimal('1.0')

    def test_mixed_value_types_in_thresholds_and_weights(self):
        thresholds = [100, 50.5, Decimal('10.1')]
        weights = [5, 3.3, Decimal('1.7')]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        result = factor.get_weight(75)
        assert result.value == 75
        assert result.weight == Decimal('3.30')

    def test_identical_thresholds(self):
        thresholds = [50, 50, 50]
        weights = [3.0, 2.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        # All thresholds are the same, so any value >= 50 should get the first weight
        assert factor.get_weight(100).weight == Decimal('3.0')
        assert factor.get_weight(50).weight == Decimal('3.0')

    def test_edge_case_very_close_values(self):
        thresholds = [10.001, 10.000, 9.999]
        weights = [3.0, 2.0, 1.0]
        factor = FactorByThreshold("test_factor", thresholds, weights)

        assert factor.get_weight(10.0005).weight == Decimal('2.0000')
        assert factor.get_weight(9.9995).weight == Decimal('1.0000')
