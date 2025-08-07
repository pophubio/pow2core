from decimal import Decimal

from ..algorithms.threshold import FactorByThreshold
from ..const import FACTOR_NAME_LISTING_COUNT, FACTOR_ALGORITHM_THRESHOLD
from ..registry import FactorRegistry
from ..schema import ListingCountFactorByThresholdConfig, FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_LISTING_COUNT,
    algorithm=FACTOR_ALGORITHM_THRESHOLD,
    config_schema=ListingCountFactorByThresholdConfig,
)
class ListingCountFactorByThreshold(FactorByThreshold):
    """使用阈值计算挂单数量权重"""
    def __init__(
        self,
        thresholds: list[int | float | Decimal],
        weights: list[int | float | Decimal],
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_LISTING_COUNT,
            thresholds=thresholds,
            weights=weights,
            **kwargs,
        )

    def get_weight(self, count: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        return super().get_weight(count)
