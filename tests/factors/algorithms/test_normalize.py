from decimal import Decimal

import pytest

from pow2core.factors.algorithms.normalize import FactorByNormalize


class TestFactorByNormalize:
    def test_init_with_provided_alpha_linear(self):
        values = [1, 2, 3, 4, 5]
        factor = FactorByNormalize("test_factor", values, alpha=1.0, method="linear")

        assert factor.name == "test_factor"
        assert factor.alpha == 1.0
        assert len(factor._weights) == 5

    def test_init_with_provided_alpha_log(self):
        values = [1, 2, 3, 4, 5]
        factor = FactorByNormalize("test_factor", values, alpha=1.0, method="log")

        assert factor.name == "test_factor"
        assert factor.alpha == 1.0
        assert len(factor._weights) == 5

    def test_init_invalid_method(self):
        values = [1, 2, 3]
        with pytest.raises(ValueError, match="Invalid normalization method: invalid"):
            FactorByNormalize("test_factor", values, method="invalid")

    def test_init_find_alpha_with_ratio(self):
        values = [1, 5, 10]
        factor = FactorByNormalize("test_factor", values, ratio=2.0, tolerance=0.5)

        assert factor.alpha is not None
        assert isinstance(factor.alpha, float)

    def test_init_find_alpha_fails(self):
        values = [1, 2, 3]
        with pytest.raises(ValueError, match="Failed to find alpha for given ratio"):
            FactorByNormalize(
                "test_factor",
                values,
                ratio=100.0,  # Impossible ratio
                tolerance=0.01,
                max_alpha=1.0
            )

    def test_load_weights_linear_method(self):
        values = [1, 2, 3]
        factor = FactorByNormalize("test_factor", values, alpha=0, method="linear")

        weights = factor.load_weights(values)

        # With alpha=0, weights should be proportional to original values
        assert len(weights) == 3
        assert all(isinstance(w, float) for w in weights.values())
        # Smallest weight should be scaled to 1.0
        assert min(weights.values()) == 1.0

    def test_load_weights_log_method(self):
        values = [1, 2, 3]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="log")

        weights = factor.load_weights(values)

        assert len(weights) == 3
        assert all(isinstance(w, float) for w in weights.values())
        assert min(weights.values()) == 1.0

    def test_load_weights_with_alpha(self):
        values = [1, 2, 3]
        factor = FactorByNormalize("test_factor", values, alpha=1.0, method="linear")

        weights_alpha_0 = factor._load_weights(values, alpha=0)
        weights_alpha_1 = factor._load_weights(values, alpha=1.0)

        # Alpha should smooth out the differences
        ratio_alpha_0 = max(weights_alpha_0.values()) / min(weights_alpha_0.values())
        ratio_alpha_1 = max(weights_alpha_1.values()) / min(weights_alpha_1.values())

        assert ratio_alpha_1 < ratio_alpha_0

    def test_get_weight_valid_value(self):
        values = [1, 2, 3]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        weight = factor.get_weight(1)
        assert weight.value == 1
        assert weight.weight > 0

    def test_get_weight_invalid_value(self):
        values = [1, 2, 3]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        with pytest.raises(ValueError, match="Value 4 not in weight nums"):
            factor.get_weight(4)

    def test_get_weight_precision_control(self):
        values = [1, 2, 3]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear", precision=3)

        weight = factor.get_weight(1)
        # Check that the result has the correct precision
        assert len(str(weight.weight).split('.')[-1]) <= 3

    def test_find_alpha_success(self):
        values = [1, 2, 4]
        factor = FactorByNormalize(
            "test_factor",
            values,
            ratio=2.0,
            min_alpha=0,
            max_alpha=5,
            alpha_step=0.1,
            tolerance=0.2,
            method="linear",
        )

        alpha = factor._find_alpha(values=values)

        assert isinstance(alpha, float)
        assert 0 <= alpha <= 5

    def test_find_alpha_boundary_conditions(self):
        values = [1, 10]
        factor = FactorByNormalize(
            "test_factor",
            values,
            ratio=5.0,
            min_alpha=0,
            max_alpha=10,
            alpha_step=1.0,
            tolerance=1.0,
            method="linear"
        )

        # Test that it can find alpha at the boundary
        alpha = factor._find_alpha(values=values)

        assert isinstance(alpha, float)

    def test_with_decimal_values(self):
        values = [Decimal('1.5'), Decimal('2.5'), Decimal('3.5')]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        weight = factor.get_weight(Decimal('1.5'))
        assert weight.value == Decimal('1.5')
        assert weight.weight > 0

    def test_mixed_value_types(self):
        values = [1, 2.5, Decimal('3.5')]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        for value in values:
            weight = factor.get_weight(value)
            assert weight.value == value
            assert weight.weight > 0

    def test_large_values(self):
        values = [1000, 2000, 3000]
        factor = FactorByNormalize("test_factor", values, alpha=100, method="linear")

        weights = [factor.get_weight(v) for v in values]
        assert all(w.weight > 0 for w in weights)

    def test_single_value(self):
        values = [5]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        weight = factor.get_weight(5)
        assert weight.value == 5
        assert weight.weight == Decimal('1.00')  # Single value should normalize to 1

    def test_identical_values(self):
        values = [3, 3, 3]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        # All weights should be identical
        weights = [factor.get_weight(3) for _ in values]
        assert all(w.weight == weights[0].weight for w in weights)

    def test_zero_values_linear(self):
        values = [0, 1, 2]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="linear")

        # Should handle zero values with alpha
        weight = factor.get_weight(0)
        assert weight.value == 0
        assert weight.weight > 0

    def test_zero_values_log(self):
        values = [0, 1, 2]
        factor = FactorByNormalize("test_factor", values, alpha=1, method="log")

        # log1p(0) = 0, so alpha helps with smoothing
        weight = factor.get_weight(0)
        assert weight.value == 0
        assert weight.weight > 0

    def test_custom_parameters(self):
        values = [1, 2, 3, 4]
        factor = FactorByNormalize(
            "test_factor",
            values,
            alpha=2.5,
            method="log",
            precision=4,
            min_alpha=1.0,
            max_alpha=5.0,
            alpha_step=0.5,
            tolerance=0.05
        )

        assert factor.alpha == 2.5
        assert factor.precision == 4

        weight = factor.get_weight(1)
        # Check precision
        decimal_places = len(str(weight.weight).split('.')[-1])
        assert decimal_places <= 4
