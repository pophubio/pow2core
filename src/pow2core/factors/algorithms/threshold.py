from decimal import Decimal

from .base import BaseFactor
from ..const import FACTOR_ALGORITHM_THRESHOLD
from ..schema import FactorWeightResult


class FactorByThreshold(BaseFactor):
    """使用阈值计算权重"""
    def __init__(
        self,
        name: str,
        thresholds: list[int | float | Decimal],
        weights: list[int | float | Decimal],
        precision: int = 2,
        max_weight: Decimal = Decimal(1),
        is_visible: bool = True,
        **kwargs,
    ):
        """
        初始化阈值计算因子
        """
        super().__init__(
            name=name,
            algorithm=FACTOR_ALGORITHM_THRESHOLD,
            precision=precision,
            max_weight=max_weight,
            is_visible=is_visible,
            **kwargs,
        )
        if len(thresholds) != len(weights):
            raise ValueError("Thresholds and weights must have the same length")

        if not thresholds or not weights:
            raise ValueError("Thresholds and weights must be provided")

        self.thresholds = sorted(thresholds, reverse=True)
        self.weights = weights

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        if not isinstance(value, int | float | Decimal):
            raise ValueError("Value must be number")

        target_weight = None
        for threshold, weight in zip(self.thresholds, self.weights, strict=True):
            if value >= threshold:
                target_weight = Decimal(str(weight))
                break
        else:
            raise ValueError(f"Value {value} less than min threshold {self.thresholds[-1]}")

        return FactorWeightResult(value=value, weight=target_weight)
