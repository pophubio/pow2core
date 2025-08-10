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
        self.tokens_with_slot: list[tuple[int, int]] = []

    def load_tokens_with_slot(self, rare_balances: dict[int, list[tuple[int, int]]]):
        """
        获取具有卡槽的tokenid列表

        Args:
            rare_balances: 按照稀有度分组的(collection_id, token_id)列表

        Returns:
            list[tuple[int, int]]: 具有卡槽的(collection_id, token_id)列表
        """
        set_count = min([
            len(rare_balances[rare]) // self.rare_requirements[rare]
            for rare in self.rare_requirements
        ])

        new_tokens_with_slot = [
            (collection_id, token_id)
            for rare in self.rare_requirements
            for collection_id, token_id in rare_balances[rare][:set_count * self.rare_requirements[rare]]
        ]
        self.tokens_with_slot.extend(new_tokens_with_slot)

    def get_weight(self, collection_id: int, token_id: int) -> FactorWeightResult:
        """
        获取token的权重
        调用之前应该调用 load_tokens_with_slot 更新 tokens_with_slot
        """
        value = (collection_id, token_id) in self.tokens_with_slot
        return super().get_weight(value)
