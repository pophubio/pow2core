import pytest
from decimal import Decimal

from pow2core.factors.algorithms.value import FactorByValue


class TestFactorByValue:
    def test_init_default_precision(self):
        """Test initialization with default precision"""
        factor = FactorByValue("test_factor")
        
        assert factor.name == "test_factor"
        assert factor.precision == 2

    def test_init_custom_precision(self):
        """Test initialization with custom precision"""
        factor = FactorByValue("test_factor", precision=4)
        
        assert factor.name == "test_factor"
        assert factor.precision == 4

    def test_get_weight_with_int_value(self):
        """Test get_weight with integer value"""
        factor = FactorByValue("test_factor")
        
        result = factor.get_weight(42)
        assert result.value == 42
        assert result.weight == Decimal('42')

    def test_get_weight_with_float_value(self):
        """Test get_weight with float value"""
        factor = FactorByValue("test_factor")
        
        result = factor.get_weight(42.5)
        assert result.value == 42.5
        assert result.weight == Decimal('42.5')

    def test_get_weight_with_decimal_value(self):
        """Test get_weight with Decimal value"""
        factor = FactorByValue("test_factor")
        
        value = Decimal('42.75')
        result = factor.get_weight(value)
        assert result.value == Decimal('42.75')
        assert result.weight == Decimal('42.75')

    def test_get_weight_with_zero_value(self):
        """Test get_weight with zero value"""
        factor = FactorByValue("test_factor")
        
        result = factor.get_weight(0)
        assert result.value == 0
        assert result.weight == Decimal('0')
        
        result = factor.get_weight(0.0)
        assert result.value == 0.0
        assert result.weight == Decimal('0.0')

    def test_get_weight_with_negative_value(self):
        """Test get_weight with negative value"""
        factor = FactorByValue("test_factor")

        result = factor.get_weight(-42)
        assert result.value == -42
        assert result.weight == Decimal('-42')

        result = factor.get_weight(-42.5)
        assert result.value == -42.5
        assert result.weight == Decimal('-42.5')

    def test_get_weight_with_large_value(self):
        """Test get_weight with large value"""
        factor = FactorByValue("test_factor")

        large_int = 999999999999999
        result = factor.get_weight(large_int)
        assert result.value == large_int
        assert result.weight == Decimal(str(large_int))

        large_float = 999999999999.999
        result = factor.get_weight(large_float)
        assert result.value == large_float
        assert result.weight == Decimal('999999999999.999')

    def test_get_weight_with_small_decimal_value(self):
        """Test get_weight with very small decimal value"""
        factor = FactorByValue("test_factor")

        small_value = Decimal('0.0000001')
        result = factor.get_weight(small_value)
        assert result.value == small_value
        assert result.weight == small_value

    def test_get_weight_with_scientific_notation(self):
        """Test get_weight with scientific notation"""
        factor = FactorByValue("test_factor")

        # Test with float in scientific notation
        sci_float = 1.23e-10
        result = factor.get_weight(sci_float)
        assert result.value == sci_float
        assert result.weight == Decimal('1.23E-10')

        # Test with Decimal in scientific notation
        sci_decimal = Decimal('1.23E-10')
        result = factor.get_weight(sci_decimal)
        assert result.value == sci_decimal
        assert result.weight == Decimal('1.23E-10')

    def test_get_weight_precision_control(self):
        """Test that precision is controlled by BaseFactor._quantize method"""
        factor = FactorByValue("test_factor", precision=3)

        # The get_weight method should return the exact value without quantization
        # since it directly returns Decimal(str(value))
        value = 42.12345
        result = factor.get_weight(value)
        assert result.value == value
        assert result.weight == Decimal(str(value))

    def test_get_weight_with_string_conversion(self):
        """Test that get_weight converts value to string then to Decimal"""
        factor = FactorByValue("test_factor")
        
        # This tests the internal conversion: Decimal(str(value))
        result = factor.get_weight(42.123456789)
        assert result.value == 42.123456789
        assert result.weight == Decimal('42.123456789')

    def test_get_weight_with_none_value(self):
        """Test get_weight with None value should raise error"""
        factor = FactorByValue("test_factor")
        
        with pytest.raises(TypeError):
            factor.get_weight(None)

    def test_get_weight_with_string_value(self):
        """Test get_weight with string value should raise error"""
        factor = FactorByValue("test_factor")
        
        with pytest.raises(TypeError):
            factor.get_weight("42")

    def test_get_weight_with_list_value(self):
        """Test get_weight with list value should raise error"""
        factor = FactorByValue("test_factor")
        
        with pytest.raises(TypeError):
            factor.get_weight([42])

    def test_get_weight_with_dict_value(self):
        """Test get_weight with dict value should raise error"""
        factor = FactorByValue("test_factor")
        
        with pytest.raises(TypeError):
            factor.get_weight({"value": 42})

    def test_quantize_method_inheritance(self):
        """Test that _quantize method is inherited from BaseFactor"""
        factor = FactorByValue("test_factor", precision=3)
        
        quantized = factor._quantize(Decimal('1.23456'))
        assert quantized == Decimal('1.235')

    def test_edge_case_very_large_float(self):
        """Test get_weight with very large float value"""
        factor = FactorByValue("test_factor")
        
        large_float = 1e308  # Very large float
        result = factor.get_weight(large_float)
        assert result.value == large_float
        assert result.weight == Decimal('1E+308')

    def test_edge_case_very_small_float(self):
        """Test get_weight with very small float value"""
        factor = FactorByValue("test_factor")

        small_float = 1e-308  # Very small float
        result = factor.get_weight(small_float)
        assert result.value == small_float
        assert result.weight == Decimal('1E-308')

    def test_multiple_instances(self):
        """Test that multiple instances work independently"""
        factor1 = FactorByValue("factor1", precision=2)
        factor2 = FactorByValue("factor2", precision=4)

        assert factor1.name == "factor1"
        assert factor2.name == "factor2"
        assert factor1.precision == 2
        assert factor2.precision == 4

        result1 = factor1.get_weight(42.123)
        result2 = factor2.get_weight(42.123)

        assert result1.value == 42.123
        assert result2.value == 42.123
