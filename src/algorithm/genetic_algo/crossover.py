# genetic_algo/crossover.py
from abc import ABC, abstractmethod

from .chromosome import Chromosome
from .parameter import GeneticAlgoParameter


class StrategyRegistry:
    strategies = {}

    @classmethod
    def register(cls, strategy) -> "Crossover":
        def decorator(subclass) -> "Crossover":
            cls.strategies[strategy] = subclass
            return subclass

        return decorator

    @classmethod
    def get_strategy(cls, strategy) -> "Crossover":
        if strategy not in cls.strategies:
            raise ValueError(f"Unknown crossover strategy {strategy}")
        return cls.strategies[strategy]


class Crossover(ABC):
    """Abstract class for Crossover."""

    @abstractmethod
    def __init__(self, parameters: GeneticAlgoParameter):
        """Initialize Crossover."""
        self.params = parameters

    @abstractmethod
    def crossover(self) -> list[Chromosome]:
        """Perform crossover."""
        pass
