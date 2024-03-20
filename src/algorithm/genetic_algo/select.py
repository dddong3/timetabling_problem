from abc import ABC, abstractmethod

from .parameter import GeneticAlgoParameter


class StrategyRegistry:
    strategies = {}

    @classmethod
    def register(cls, strategy) -> "Select":
        def decorator(subclass) -> "Select":
            cls.strategies[strategy] = subclass
            return subclass

        return decorator

    @classmethod
    def get_strategy(cls, strategy) -> "Select":
        if strategy not in cls.strategies:
            raise ValueError(f"Unknown select strategy {strategy}")
        return cls.strategies[strategy]


class Select(ABC):
    """Abstract class for Selection."""

    @abstractmethod
    def __init__(self, parameters: GeneticAlgoParameter):
        """Initialize Selection."""
        self.params = parameters

    @abstractmethod
    def select(self):
        """Perform selection."""
        pass
