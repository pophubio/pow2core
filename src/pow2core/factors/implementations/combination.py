from decimal import Decimal

from ..algorithms.value import FactorByValue
from ..const import FACTOR_NAME_COMBINATION, FACTOR_ALGORITHM_VALUE
from ..registry import FactorRegistry
from ..schema import CombinationFactorByValueConfig, FactorWeightResult


@FactorRegistry.register(
    name=FACTOR_NAME_COMBINATION,
    algorithm=FACTOR_ALGORITHM_VALUE,
    config_schema=CombinationFactorByValueConfig,
)
class CombinationFactorByValue(FactorByValue):
    """使用值计算变压器权重"""
    def __init__(
        self,
        precision: int = 3,
        max_weight: Decimal = Decimal(1),
        is_visible: bool = True,
        **kwargs,
    ):
        super().__init__(
            name=FACTOR_NAME_COMBINATION,
            precision=precision,
            max_weight=max_weight,
            is_visible=is_visible,
            **kwargs,
        )

    def get_weight(self, ratio: int | float | Decimal) -> FactorWeightResult:
        """获取权重"""
        return super().get_weight(ratio)
