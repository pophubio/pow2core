from decimal import Decimal

from ..algorithms.fixed import FactorByFixed
from ..const import FACTOR_NAME_IS_LISTING, FACTOR_ALGORITHM_FIXED
from ..registry import FactorRegistry
from ..schema import FactorWeightResult, IsListingFactorByFixedConfig


@FactorRegistry.register(
    name=FACTOR_NAME_IS_LISTING,
    algorithm=FACTOR_ALGORITHM_FIXED,
    config_schema=IsListingFactorByFixedConfig,
)
class IsListingFactorByFixed(FactorByFixed):
    """是否正在挂单"""
    def __init__(
        self,
        weights: dict[bool, int | Decimal],
        precision: int = 2,
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_IS_LISTING,
            weights=weights,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, is_listing: bool) -> FactorWeightResult:
        return super().get_weight(is_listing)
