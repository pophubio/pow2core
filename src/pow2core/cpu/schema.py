from decimal import Decimal

from pydantic import BaseModel, Field

from ..factors.schema import FactorWeightResult


class CPUResult(BaseModel):
    """CPU计算结果"""
    cpu: Decimal = Field(description="最终CPU值")
    factor_weights: dict[str, FactorWeightResult] = Field(description="所有权重")
