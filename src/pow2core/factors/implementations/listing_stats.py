from datetime import datetime
from decimal import Decimal

from ..const import FACTOR_NAME_LISTING_STATS
from .listing_days import ListingDaysFactorByLinear
from .listing_count import ListingCountFactorByThreshold
from ..registry import FactorRegistry
from ..schema import FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_LISTING_STATS,
)
class ListingStatsFactor:
    """
    挂单统计因子是由挂单天数和挂单数量共同决定的
    如果挂单数量权重小于1, 则使用挂单数量作为权重, 否则使用挂单天数作为权重
    """
    def __init__(
        self,
        listing_days_factor: ListingDaysFactorByLinear,
        listing_count_factor: ListingCountFactorByThreshold,
        **kwargs,
    ):
        self.name = FACTOR_NAME_LISTING_STATS
        self.listing_days_factor = listing_days_factor
        self.listing_count_factor = listing_count_factor
        self.kwargs = kwargs

    def get_weight(self, listing_start_at: datetime, listing_count: int | Decimal) -> FactorWeightResult:
        """获取权重"""
        result = FactorWeightResult(value=Decimal(0), weight=Decimal(0), children={})

        listing_count_weight = self.listing_count_factor.get_weight(listing_count)
        result.children[self.listing_count_factor.name] = listing_count_weight
        listing_days_weight = self.listing_days_factor.get_weight(listing_start_at)
        result.children[self.listing_days_factor.name] = listing_days_weight

        if listing_count_weight.weight < 1:
            result.value = listing_count_weight.value
            result.weight = listing_count_weight.weight
        else:
            result.value = listing_days_weight.value
            result.weight = listing_days_weight.weight

        return result
