from decimal import Decimal

from ..algorithms.fixed import FactorByFixed
from ..const import FACTOR_NAME_POP_USER, FACTOR_ALGORITHM_FIXED
from ..registry import FactorRegistry
from ..schema import FactorWeightResult, POPUserFactorByFixedConfig


@FactorRegistry.register(
    name=FACTOR_NAME_POP_USER,
    algorithm=FACTOR_ALGORITHM_FIXED,
    config_schema=POPUserFactorByFixedConfig,
)
class POPUserFactorByFixed(FactorByFixed):
    """POP用户"""
    def __init__(
        self,
        weights: dict[bool, int | Decimal],
        precision: int = 2,
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_POP_USER,
            weights=weights,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, is_pop_user: bool) -> FactorWeightResult:
        return super().get_weight(is_pop_user)
