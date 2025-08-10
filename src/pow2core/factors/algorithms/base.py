"""
Factors Module

This module provides different types of factor calculation algorithms.
"""

from abc import ABC
from decimal import Decimal
from typing import Protocol

from ..schema import FactorWeightResult


class Factor(Protocol):
    """Protocol for factors"""
    @property
    def name(self) -> str:
        """Get the name of the factor"""
        ...

    @property
    def algorithm(self) -> str:
        """Get the algorithm of the factor"""
        ...

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:
        """Get weight of factor for the given value"""
        ...


class BaseFactor(ABC):  # noqa: B024
    """Base class for weight factors"""
    def __init__(self, name: str, algorithm: str, precision: int = 2, **kwargs):
        self.name = name
        self.algorithm = algorithm
        self.precision = precision
        self.kwargs = kwargs

    def get_weight(self, value: int | float | Decimal) -> FactorWeightResult:  # noqa: B027
        """Get weight of factor for the given value"""
        pass

    def _quantize(self, num) -> Decimal:
        quantize_str = f"1.{'0' * self.precision}"
        return Decimal(str(num)).quantize(Decimal(quantize_str))
