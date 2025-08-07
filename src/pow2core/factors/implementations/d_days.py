from decimal import Decimal
from datetime import datetime, timezone, timedelta

from ..algorithms.normalize import FactorByNormalize
from ..const import FACTOR_NAME_DDAYS, NORMALIZE_METHOD_LINEAR, FACTOR_ALGORITHM_NORMALIZE
from ..registry import FactorRegistry
from ..schema import DDaysFactorByNormalizeConfig, FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_DDAYS,
    algorithm=FACTOR_ALGORITHM_NORMALIZE,
    method=NORMALIZE_METHOD_LINEAR,
    config_schema=DDaysFactorByNormalizeConfig,
)
class DDaysFactorByLinearNormalize(FactorByNormalize):
    """使用线性归一化计算天数权重"""
    def __init__(
        self,
        created_at: datetime,
        multiplier: Decimal,
        now: datetime,
        tz_hours: int = 8,  # 默认是北京时区
        precision: int = 2,
        **kwargs,
    ):
        self.tz = timezone(timedelta(hours=tz_hours))
        self.now = self.convert_to_tz(now)
        self.created_at = self.convert_to_tz(created_at)

        max_days = (self.now - self.created_at).days + 1  # 从1开始, 不足1天算1天
        days = list(range(1, max_days + 1))

        super().__init__(
            name=FACTOR_NAME_DDAYS,
            values=days,
            alpha=max_days * multiplier,
            method=NORMALIZE_METHOD_LINEAR,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, start_at: datetime) -> FactorWeightResult:
        start_at = self.convert_to_tz(start_at)
        days = (self.now - start_at).days + 1
        days = max(days, 1)
        return super().get_weight(days)

    def convert_to_tz(self, dt: datetime) -> datetime:
        return dt.astimezone(tz=self.tz)
