from decimal import Decimal

from ..algorithms.fixed import FactorByFixed
from ..algorithms.normalize import FactorByNormalize
from ..const import FACTOR_NAME_RARE, NORMALIZE_METHOD_LINEAR, FACTOR_ALGORITHM_FIXED, FACTOR_ALGORITHM_NORMALIZE
from ..registry import FactorRegistry
from ..schema import FactorWeightResult, RareFactorByFixedConfig, RareFactorByNormalizeConfig


@FactorRegistry.register(
    name=FACTOR_NAME_RARE,
    algorithm=FACTOR_ALGORITHM_FIXED,
    config_schema=RareFactorByFixedConfig,
)
class RareFactorByFixed(FactorByFixed):
    """OG卡使用稀有度固定权重"""
    def __init__(self, weights: dict[int | Decimal, int | Decimal], precision: int = 2, **kwargs):
        super().__init__(name=FACTOR_NAME_RARE, weights=weights, precision=precision, **kwargs)


@FactorRegistry.register(
    name=FACTOR_NAME_RARE,
    algorithm=FACTOR_ALGORITHM_NORMALIZE,
    method=NORMALIZE_METHOD_LINEAR,
    config_schema=RareFactorByNormalizeConfig,
)
class RareFactorByLinearNormalize(FactorByNormalize):
    """GCW使用稀有度归一化权重"""
    def __init__(
        self,
        min_rare: int,
        max_rare: int,
        alpha: int,
        precision: int = 2,
        **kwargs,
    ):
        self.min_rare = min_rare
        self.max_rare = max_rare
        # 稀有度低的权重高
        rares = list(range(min_rare, max_rare+1))

        super().__init__(
            name=FACTOR_NAME_RARE,
            values=rares,
            alpha=alpha,
            method=NORMALIZE_METHOD_LINEAR,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, rare: int) -> FactorWeightResult:
        """获取权重"""
        value = self.max_rare - rare + 1
        return super().get_weight(value)
