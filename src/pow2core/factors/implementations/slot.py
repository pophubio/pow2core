from decimal import Decimal

from ..algorithms.fixed import FactorByFixed
from ..const import FACTOR_NAME_SLOT, FACTOR_ALGORITHM_FIXED
from ..registry import FactorRegistry
from ..schema import FactorWeightResult, SlotFactorByFixedConfig


@FactorRegistry.register(
    name=FACTOR_NAME_SLOT,
    algorithm=FACTOR_ALGORITHM_FIXED,
    config_schema=SlotFactorByFixedConfig,
)
class SlotFactorByFixed(FactorByFixed):
    """卡槽"""
    def __init__(
        self,
        weights: dict[bool, int | Decimal],
        rare_requirements: dict[int, int],
        precision: int = 2,
        **kwargs,
    ):
        self.rare_requirements = rare_requirements
        super().__init__(
            name=FACTOR_NAME_SLOT,
            weights=weights,
            precision=precision,
            **kwargs,
        )
        self.token_ids_with_slot = []

    def update_tokens_with_slot(self, rare_balances: dict[int, list[int]]) -> list[int]:
        """
        获取具有卡槽的tokenid列表

        Args:
            rare_balances: 按照稀有度分组的tokenid列表

        Returns:
            list[int]: 具有卡槽的tokenid列表
        """
        set_count = min([
            len(rare_balances[rare]) // self.rare_requirements[rare]
            for rare in self.rare_requirements
        ])

        new_token_ids = [
            token_id
            for rare in self.rare_requirements
            for token_id in rare_balances[rare][:set_count * self.rare_requirements[rare]]
        ]
        self.token_ids_with_slot.extend(new_token_ids)

    def get_weight(self, token_id: int) -> FactorWeightResult:
        """
        获取token的权重
        调用之前应该调用 update_tokens_with_slot 更新 token_ids_with_slot

        Args:
            value: 是token_id

        Returns:
            Decimal: 权重
        """
        value = token_id in self.token_ids_with_slot
        return super().get_weight(value)
