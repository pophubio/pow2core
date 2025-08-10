from datetime import datetime, timezone

from .schema import CPUResult
from ..config.schema import CPUConfig, FactorConfig
from ..factors.algorithms.base import Factor
from ..factors.const import FACTOR_NAME_DDAYS, FACTOR_NAME_LISTING_DAYS


class CPUCalculator:
    """CPU计算器"""

    def __init__(self, config: CPUConfig, now: datetime | None = None):
        """初始化CPU计算器"""
        self.config = config
        self.now = now or datetime.now(timezone.utc)  # noqa: UP017

        self.factors: dict[str, Factor] = {}

    def load_factors(self) -> None:
        """加载所有因子"""
        for factor_config in self.config.factors:
            if factor_config.children:
                children_factors = {
                    f"{child.name}_factor": self.load_factor(child)
                    for child in factor_config.children
                }
                factor = factor_config.implementation(**children_factors)
                self.add_factor(factor)
            else:
                factor = self.load_factor(factor_config)
                self.add_factor(factor)

    def load_factor(self, factor_config: FactorConfig) -> Factor:
        """加载某个因子"""
        impl_config = factor_config.config.model_dump() if factor_config.config else {}
        if "method" in impl_config:
            impl_config.pop("method")

        if "algorithm" in impl_config:
            impl_config.pop("algorithm")

        if factor_config.name in [FACTOR_NAME_DDAYS, FACTOR_NAME_LISTING_DAYS]:
            impl_config["now"] = self.now

        factor = factor_config.implementation(**impl_config)
        return factor

    def add_factor(self, factor: Factor) -> None:
        """添加一个因子至计算器"""
        self.factors[factor.name] = factor

    def remove_factor(self, factor_name: str) -> None:
        """从计算器中移除一个因子"""
        if factor_name in self.factors:
            del self.factors[factor_name]

    def calculate(self, values: dict[str, dict]) -> CPUResult:
        """
        使用所有添加的因子计算CPU值

        Args:
            values: 因子值字典, 使用关键字参数

        Returns:
            CPUResult: 包含最终CPU值和所有权重的结果
        """
        result = CPUResult(cpu=self.config.base, factor_weights={})

        for factor_name, factor in self.factors.items():
            if factor_name not in values:
                raise ValueError(f"Factor {factor_name} not in values")

            params = values[factor_name]
            if not isinstance(params, dict):
                raise ValueError(f"Factor {factor_name} params must be a dict")

            factor_weight_result = factor.get_weight(**params)

            result.factor_weights[factor_name] = factor_weight_result
            result.cpu *= factor_weight_result.weight

        return result
