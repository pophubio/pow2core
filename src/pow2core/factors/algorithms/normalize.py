from decimal import Decimal
from typing import Literal

import numpy as np

from .base import BaseFactor
from ..const import NORMALIZE_METHOD_LINEAR, NORMALIZE_METHOD_LOG, FACTOR_ALGORITHM_NORMALIZE
from ..schema import FactorWeightResult


class FactorByNormalize(BaseFactor):
    """
    通过归一化计算权重, 并设置了平滑因子alpha
    如果初始化时提供了alpha, 则直接使用该alpha, 否则在alpha允许的范围内步进找到合适的alpha
    如果初始提供了待归一化的数据values, 则直接使用values加载权重, 否则需要调用load_weights方法加载权重
    """
    def __init__(
        self,
        name: str,
        values: list[int | float | Decimal] | None = None,
        alpha: int | None = None,
        method: Literal[NORMALIZE_METHOD_LINEAR, NORMALIZE_METHOD_LOG] = NORMALIZE_METHOD_LINEAR,
        ratio: float | None = None,
        min_alpha: float = 0,
        max_alpha: float = 10,
        alpha_step: float = 0.1,
        tolerance: float = 0.1,
        precision: int = 2,
        **kwargs,
    ):
        """
        初始化归一化计算因子

        Args:
            name: 因子名称
            values: 待归一化的数据
            alpha: 平滑因子, 如果为None, 则自动计算
            method: 归一化方法
            ratio: 归一化比例
            min_alpha: 最小平滑因子
            max_alpha: 最大平滑因子
            alpha_step: 平滑因子步长
            tolerance: 归一化比例误差
            precision: 权重精度
        """
        super().__init__(name, FACTOR_ALGORITHM_NORMALIZE, precision, **kwargs)

        if method not in (NORMALIZE_METHOD_LINEAR, NORMALIZE_METHOD_LOG):
            raise ValueError(f"Invalid normalization method: {method}")

        self.alpha = alpha
        self.ratio = ratio
        self.method = method
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.alpha_step = alpha_step
        self.tolerance = tolerance
        self.values = values
        if self.values:
            self._weights = self.load_weights(values=self.values)
        else:
            self._weights = None

    def load_weights(self, values: list[int | float | Decimal]) -> dict[int | float | Decimal, int | float]:
        """加载权重"""
        alpha = self._find_alpha(values=values)
        return self._load_weights(values=values, alpha=alpha)

    def _load_weights(
        self,
        values: list[int | float | Decimal],
        alpha: float,
    ) -> dict[int | float | Decimal, int | float]:
        """使用alpha加载权重"""
        if values is None:
            raise ValueError("Values must be provided")

        float_values = [float(value) for value in values]
        data = np.array(float_values)

        if self.method == NORMALIZE_METHOD_LINEAR:
            data = data + alpha
            normalized_weights = data / np.sum(data)
        elif self.method == NORMALIZE_METHOD_LOG:
            data = np.log1p(data) + alpha
            normalized_weights = data / np.sum(data)
        else:
            raise ValueError(f"Invalid normalization method: {self.method}")

        min_weight = np.min(normalized_weights)
        scaled_weights = normalized_weights / min_weight
        weights = scaled_weights.tolist()
        self._weights = dict(zip(values, weights, strict=True))
        return self._weights

    def _find_alpha(
        self,
        values: list[int | float | Decimal],
    ) -> float:
        """找到合适的alpha"""
        if self.alpha is not None:
            return self.alpha

        alpha = self.min_alpha
        while alpha < self.max_alpha:
            if not alpha:
                alpha += self.alpha_step
                continue

            weights = self._load_weights(values=values, alpha=alpha)
            actual_ratio = max(weights.values()) / min(weights.values())
            if abs(actual_ratio - self.ratio) < self.tolerance:
                self.alpha = alpha
                return alpha
            alpha += self.alpha_step
        else:  # noqa: PLW0120
            raise ValueError(f"Failed to find alpha for given ratio {self.ratio} with tolerance {self.tolerance}")

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        if value not in self._weights:
            raise ValueError(f"Value {value} not in weight nums")
        weight = self._quantize(self._weights[value])
        return FactorWeightResult(value=value, weight=weight)

