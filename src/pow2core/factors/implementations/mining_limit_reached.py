from decimal import Decimal

from ..algorithms.fixed import FactorByFixed
from ..const import FACTOR_NAME_MINING_LIMIT_REACHED, FACTOR_ALGORITHM_FIXED
from ..registry import FactorRegistry
from ..schema import FactorWeightResult, MiningLimitReachedFactorByFixedConfig


@FactorRegistry.register(
    name=FACTOR_NAME_MINING_LIMIT_REACHED,
    algorithm=FACTOR_ALGORITHM_FIXED,
    config_schema=MiningLimitReachedFactorByFixedConfig,
)
class MiningLimitReachedFactorByFixed(FactorByFixed):
    """是否达到挖矿上限"""
    def __init__(
        self,
        weights: dict[bool, int | Decimal],
        precision: int = 2,
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_MINING_LIMIT_REACHED,
            weights=weights,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, is_reached: bool) -> FactorWeightResult:
        return super().get_weight(is_reached)
