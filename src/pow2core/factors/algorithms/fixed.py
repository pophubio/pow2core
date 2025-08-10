from decimal import Decimal

from .base import BaseFactor
from ..schema import FactorWeightResult
from ..const import FACTOR_ALGORITHM_FIXED


class FactorByFixed(BaseFactor):
    """使用固定字典计算权重"""
    def __init__(self, name: str, weights: dict[int | Decimal, int | Decimal], precision: int = 2, **kwargs):
        """
        初始化固定因子

        Args:
            name: Factor name
            weights: Dictionary of weights: {value: weight}
        """
        super().__init__(name, FACTOR_ALGORITHM_FIXED, precision, **kwargs)
        if not weights:
            raise ValueError("Weights must be provided")
        self.weights = weights

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        if not isinstance(value, int | float | Decimal):
            raise ValueError("Value must be number")
        if value not in self.weights:
            raise ValueError(f"Value {value} not in weight keys")
        weight = self._quantize(self.weights[value])
        return FactorWeightResult(value=value, weight=weight)
