from decimal import Decimal

from ..algorithms.linear import FactorByLinear
from ..algorithms.normalize import FactorByNormalize
from ..const import FACTOR_NAME_VOLUME, NORMALIZE_METHOD_LOG, FACTOR_ALGORITHM_LINEAR, FACTOR_ALGORITHM_NORMALIZE
from ..registry import FactorRegistry
from ..schema import VolumeFactorByLinearConfig, VolumeFactorByNormalizeConfig, FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_VOLUME,
    algorithm=FACTOR_ALGORITHM_LINEAR,
    config_schema=VolumeFactorByLinearConfig,
)
class VolumeFactorByLinear(FactorByLinear):
    """使用线性计算交易量权重"""
    def __init__(
        self,
        min_volume: Decimal,
        max_volume: Decimal,
        min_weight: Decimal = Decimal("1.00"),
        max_weight: Decimal = Decimal("5.00"),
        precision: int = 2,
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_VOLUME,
            min_value=min_volume,
            max_value=max_volume,
            min_weight=min_weight,
            max_weight=max_weight,
            precision=precision,
            **kwargs,
        )


@FactorRegistry.register(
    name=FACTOR_NAME_VOLUME,
    algorithm=FACTOR_ALGORITHM_NORMALIZE,
    method=NORMALIZE_METHOD_LOG,
    config_schema=VolumeFactorByNormalizeConfig,
)
class VolumeFactorByLogNormalize(FactorByNormalize):
    """使用对数归一化计算交易量权重"""
    def __init__(
        self,
        ratio: float,
        min_alpha: float,
        max_alpha: float,
        alpha_step: float,
        tolerance: float,
        precision: int = 2,
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_VOLUME,
            method=NORMALIZE_METHOD_LOG,
            ratio=ratio,
            min_alpha=min_alpha,
            max_alpha=max_alpha,
            alpha_step=alpha_step,
            tolerance=tolerance,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, volume: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        return super().get_weight(volume)
