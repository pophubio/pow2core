from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, Field

from ..distribute_strategies.schema import FixedGroupStrategyConfig, LevelGroupStrategyConfig
from ..factors.algorithms.base import BaseFactor
from ..factors.implementations.listing import ListingFactor
from ..factors.schema import BaseFactorConfig


class CollectionConfig(BaseModel):
    """合集配置"""
    slugs: list[str] = Field(description="合集slug列表")


class SeasonConfig(BaseModel):
    """赛季配置"""
    slug: str = Field(description="赛季slug")
    title: str = Field(description="赛季标题")
    start_at: datetime = Field(description="赛季开始时间")
    epoch_hours: int = Field(description="每个周期的小时数")
    max_epoch: int = Field(description="最大周期数")
    priority: int = Field(description="优先级")
    per_epoch_diamonds: int = Field(description="每个周期钻石数量")
    inviter_diamond_reward_ratio: Decimal = Field(description="邀请者钻石奖励比例", default=Decimal(0))

    @field_validator("start_at", mode="before")
    @classmethod
    def isoformat(cls, v: str) -> datetime:
        return datetime.fromisoformat(v)


class FactorConfig(BaseModel):
    """因子配置"""
    name: str = Field(description="因子名称")
    priority: int = Field(description="优先级")
    implementation: type[BaseFactor] | type[ListingFactor] = Field(description="实现类")
    config: BaseFactorConfig | None = Field(default=None, description="因子配置")
    children: list['FactorConfig'] | None = Field(default=None, description="子因子")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CPUConfig(BaseModel):
    """CPU配置"""
    base: int = Field(description="基础CPU值")
    factors: list[FactorConfig] = Field(description="因子列表")


class CombinationComponentConfig(BaseModel):
    """变压器组件配置"""
    collection_slug: str = Field(description="合集slug")
    token_id: int = Field(description="token id")
    min_amount: int = Field(description="最小数量")
    max_amount: int = Field(description="最大数量")
    per_ratio: Decimal = Field(description="每比例")
    is_enable: bool = Field(description="是否启用")
    enable_at: datetime | None = Field(default=None, description="启用时间")

    @field_validator("enable_at", mode="before")
    @classmethod
    def isoformat(cls, v: str | None) -> datetime | None:
        if v is None:
            return
        return datetime.fromisoformat(v)


class CombinationConfig(BaseModel):
    """变压器配置"""
    name: str = Field(description="变压器名称")
    base_ratio: Decimal = Field(description="基础比例")
    max_ratio: Decimal = Field(description="最大比例")
    components: list[CombinationComponentConfig] = Field(description="组合组件列表")


class DiamondConfig(BaseModel):
    """钻石配置"""
    strategy: str = Field(description="钻石分配策略")
    config: FixedGroupStrategyConfig | LevelGroupStrategyConfig = Field(description="钻石分配策略配置")


class MineSeasonConfig(BaseModel):
    """挖钻赛季配置"""
    collection: CollectionConfig = Field(description="合集")
    category: str = Field(description="分类")
    image: str = Field(description="图片")
    season: SeasonConfig = Field(description="赛季")
    cpu: CPUConfig = Field(description="CPU配置")
    diamond: DiamondConfig = Field(description="钻石配置")
    combination: CombinationConfig = Field(description="组合配置")
