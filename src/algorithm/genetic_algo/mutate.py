from abc import ABC, abstractmethod

from .parameter import GeneticAlgoParameter


class StrategyRegistry:
    strategies = {}

    @classmethod
    def register(cls, strategy) -> "Mutate":
        def decorator(subclass) -> "Mutate":
            cls.strategies[strategy] = subclass
            return subclass

        return decorator

    @classmethod
    def get_strategy(cls, strategy) -> "Mutate":
        if strategy not in cls.strategies:
            raise ValueError(f"Unknown mutate strategy {strategy}")
        return cls.strategies[strategy]


class Mutate(ABC):
    """Abstract class for Mutation."""

    @abstractmethod
    def __init__(self, parameters: GeneticAlgoParameter):
        """Initialize Mutation."""
        self.params = parameters

    @abstractmethod
    def mutate(self):
        """Perform mutation."""
        pass
