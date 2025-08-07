from datetime import datetime, timezone, timedelta
from decimal import Decimal

from ..algorithms.linear import FactorByLinear
from ..const import FACTOR_NAME_LISTING_DAYS, FACTOR_ALGORITHM_LINEAR
from ..registry import FactorRegistry
from ..schema import ListingDaysFactorByLinearConfig, FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_LISTING_DAYS,
    algorithm=FACTOR_ALGORITHM_LINEAR,
    config_schema=ListingDaysFactorByLinearConfig,
)
class ListingDaysFactorByLinear(FactorByLinear):
    """使用线性计算挂单天数权重"""
    def __init__(
        self,
        now: datetime,
        min_listing_days: int,
        max_listing_days: int,
        tz_hours: int = 8,  # 默认是北京时区
        min_weight: Decimal = Decimal("1.00"),
        max_weight: Decimal = Decimal("5.00"),
        precision: int = 2,
        **kwargs,
    ):
        self.tz = timezone(timedelta(hours=tz_hours))
        self.now = self.convert_to_tz(now)
        super().__init__(
            name=FACTOR_NAME_LISTING_DAYS,
            min_value=min_listing_days,
            max_value=max_listing_days,
            min_weight=min_weight,
            max_weight=max_weight,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, start_at: datetime | None) -> FactorWeightResult:
        """获取权重"""
        if not start_at:
            return FactorWeightResult(value=0, weight=Decimal(self.max_weight))

        start_at = self.convert_to_tz(start_at)
        days = (self.now - start_at).days + 1
        days = max(days, 1)
        return super().get_weight(days)

    def convert_to_tz(self, dt: datetime) -> datetime:
        """转换时区"""
        return dt.astimezone(tz=self.tz)
