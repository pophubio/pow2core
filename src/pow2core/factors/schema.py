from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator, Field


class BaseFactorConfig(BaseModel):
    """因子配置基类"""
    algorithm: str = Field(description="算法")
    precision: int = Field(description="精度", default=2)


class AssetFactorByNormalizeConfig(BaseFactorConfig):
    """使用对数归一化计算资产权重配置"""
    method: str = Field(description="归一化方法")
    ratio: float = Field(description="期望最大最小值的比例")
    min_alpha: float = Field(description="最小alpha")
    max_alpha: float = Field(description="最大alpha")
    alpha_step: float = Field(description="alpha步长")
    tolerance: float = Field(description="alpha查找的容差")


class CombinationFactorByValueConfig(BaseFactorConfig):
    """使用值计算变压器权重配置"""
    interval: Decimal = Field(description="组合因子值的间隔")


class SlotFactorByFixedConfig(BaseFactorConfig):
    """使用固定值计算卡槽权重配置"""
    weights: dict[bool, int | Decimal] = Field(description="值与权重的映射")
    rare_requirements: dict[int, int] = Field(description="稀有度要求")


class DDaysFactorByNormalizeConfig(BaseFactorConfig):
    """使用线性归一化计算天数权重配置"""
    method: str = Field(description="归一化方法")
    multiplier: float = Field(description="乘数, 用于生成归一化的alpha")
    created_at: datetime = Field(description="合集的创建时间")
    tz_hours: int = Field(description="时区偏移", default=8)

    @field_validator("created_at", mode="before")
    @classmethod
    def isoformat(cls, v: str) -> datetime:
        return datetime.fromisoformat(v)


class ListingCountFactorByThresholdConfig(BaseFactorConfig):
    """使用阈值计算挂单数量权重配置"""
    thresholds: list[int | float | Decimal] = Field(description="阈值列表")
    weights: list[int | float | Decimal] = Field(description="权重列表")


class ListingDaysFactorByLinearConfig(BaseFactorConfig):
    """使用线性计算挂单天数权重配置"""
    min_listing_days: int = Field(description="最小挂单天数")
    max_listing_days: int = Field(description="最大挂单天数")
    min_weight: Decimal = Field(description="最小权重")
    max_weight: Decimal = Field(description="最大权重")
    tz_hours: int = Field(description="时区偏移", default=8)


class RareFactorByFixedConfig(BaseFactorConfig):
    """使用固定值计算稀有度权重配置"""
    weights: dict[int | Decimal, int | Decimal] = Field(description="稀有度与权重的映射")


class RareFactorByNormalizeConfig(BaseFactorConfig):
    """使用归一化计算稀有度权重配置"""
    method: str = Field(description="归一化方法")
    min_rare: int = Field(description="最小稀有度")
    max_rare: int = Field(description="最大稀有度")
    alpha: float = Field(description="alpha值")


class VolumeFactorByLinearConfig(BaseFactorConfig):
    """使用线性计算交易量权重配置"""
    min_volume: Decimal = Field(description="最小交易量")
    max_volume: Decimal = Field(description="最大交易量")
    min_weight: Decimal = Field(description="最小权重")
    max_weight: Decimal = Field(description="最大权重")


class VolumeFactorByNormalizeConfig(BaseFactorConfig):
    """使用对数归一化计算交易量权重配置"""
    method: str = Field(description="归一化方法")
    ratio: float = Field(description="期望最大最小值的比例")
    min_alpha: float = Field(description="最小alpha")
    max_alpha: float = Field(description="最大alpha")
    alpha_step: float = Field(description="alpha步长")
    tolerance: float = Field(description="alpha查找的容差")


class FactorWeightResult(BaseModel):
    """因子权重结果"""
    value: int | float | Decimal = Field(description="因子值")
    weight: Decimal = Field(description="权重")
    children: dict[str, 'FactorWeightResult'] | None = Field(default=None, description="子因子权重结果")
