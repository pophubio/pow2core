from decimal import Decimal

from .base import BaseFactor
from ..const import FACTOR_ALGORITHM_VALUE
from ..schema import FactorWeightResult


class FactorByValue(BaseFactor):
    """值就是权重"""
    def __init__(
        self,
        name: str,
        precision: int = 2,
        max_weight: Decimal = Decimal(1),
        is_visible: bool = True,
        **kwargs,
    ):
        """
        初始化值因子
        """
        super().__init__(
            name=name,
            algorithm=FACTOR_ALGORITHM_VALUE,
            precision=precision,
            max_weight=max_weight,
            is_visible=is_visible,
            **kwargs,
        )

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        if not isinstance(value, int | float | Decimal):
            raise TypeError("Value must be a number")

        weight = Decimal(str(value))
        return FactorWeightResult(value=value, weight=weight)
