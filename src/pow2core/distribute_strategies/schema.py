from decimal import Decimal

from pydantic import BaseModel, Field


class FixedGroupStrategyConfig(BaseModel):
    """固定组策略配置"""
    user_groups: list[int] = Field(description="用户组")
    diamond_groups: list[int] = Field(description="钻石组")
    strict: bool = Field(description="是否严格检查用户数量", default=False)


class LevelGroupThresholdItem(BaseModel):
    """等级组阈值项"""
    level: int = Field(description="等级")
    users: int = Field(description="用户数量")
    diamonds: int = Field(description="钻石数量")


class LevelGroupStrategyConfig(BaseModel):
    """等级组策略配置"""
    thresholds: list[LevelGroupThresholdItem] = Field(description="等级阈值列表")
    group_ratios: list[Decimal] = Field(description="组比例列表")
    base_group_diamonds: list[int] = Field(description="基础组钻石数量列表")
