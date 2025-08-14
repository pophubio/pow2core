from decimal import Decimal

from .base import BaseFactor
from ..schema import FactorWeightResult
from ..const import FACTOR_ALGORITHM_LINEAR


class FactorByLinear(BaseFactor):
    """根据固定系数进行线性计算"""
    def __init__(
        self,
        name: str,
        min_value: int | float | Decimal,
        max_value: int | float | Decimal,
        min_weight: int | float | Decimal = Decimal("1.00"),
        max_weight: int | float | Decimal = Decimal("5.00"),
        precision: int = 2,
        is_visible: bool = True,
        **kwargs,
    ):
        """
        初始化线性计算因子

        Args:
            name: 因子名称
            min_value: 最小值 (包含)
            max_value: 最大值 (包含)
            min_weight: 最小权重 (default: 1.00)
            max_weight: 最大权重 (default: 5.00)
            precision: 权重精度 (default: 2)
        """
        super().__init__(
            name=name,
            algorithm=FACTOR_ALGORITHM_LINEAR,
            precision=precision,
            is_visible=is_visible,
            **kwargs,
        )
        self.max_value = Decimal(str(max_value))
        self.min_weight = Decimal(str(min_weight))
        self.max_weight = Decimal(str(max_weight))
        self.min_value = Decimal(str(min_value))

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:
        """
        根据公式计算权重:
        y = min_weight + (max_weight - min_weight) / (max_value - min_value) * (x - min_value) for min_value <= x <= max_value
        y = min_weight for x < min_value
        y = max_weight for x > max_value
        where:
        - y: 权重
        - x: 输入值

        Args:
            value: 输入值

        Returns:
            FactorWeightResult: 权重结果
        """
        if not isinstance(value, int | float | Decimal):
            raise ValueError("Value must be number")

        value = Decimal(str(value))

        if value <= self.min_value:
            weight = self.min_weight
        elif value >= self.max_value:
            weight = self.max_weight
        else:
            multiplier = (self.max_weight - self.min_weight) / (self.max_value - self.min_value)
            weight = self.min_weight + multiplier * (value - self.min_value)
            weight = self._quantize(weight)

        return FactorWeightResult(value=value, weight=weight)
