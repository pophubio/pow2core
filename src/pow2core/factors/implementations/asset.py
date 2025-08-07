from decimal import Decimal

from ..algorithms.normalize import FactorByNormalize
from ..const import FACTOR_NAME_ASSET, NORMALIZE_METHOD_LOG, FACTOR_ALGORITHM_NORMALIZE
from ..registry import FactorRegistry
from ..schema import AssetFactorByNormalizeConfig, FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_ASSET,
    algorithm=FACTOR_ALGORITHM_NORMALIZE,
    method=NORMALIZE_METHOD_LOG,
    config_schema=AssetFactorByNormalizeConfig,
)
class AssetFactorByLogNormalize(FactorByNormalize):
    """使用对数归一化计算资产权重"""
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
            name=FACTOR_NAME_ASSET,
            method=NORMALIZE_METHOD_LOG,
            ratio=ratio,
            min_alpha=min_alpha,
            max_alpha=max_alpha,
            alpha_step=alpha_step,
            tolerance=tolerance,
            precision=precision,
            **kwargs,
        )

    def get_weight(self, asset: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        return super().get_weight(asset)
