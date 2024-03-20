from abc import ABC, abstractmethod
from functools import total_ordering

from .parameter import GeneticAlgoParameter


class ChromosomeRegistry:
    strategies = {}

    @classmethod
    def register(cls, strategy) -> "Chromosome":
        def decorator(subclass) -> "Chromosome":
            cls.strategies[strategy] = subclass
            return subclass

        return decorator

    @classmethod
    def get_strategy(cls, strategy) -> "Chromosome":
        if strategy not in cls.strategies:
            raise ValueError(f"Unknown chromosome strategy {strategy}")
        return cls.strategies[strategy]


@total_ordering
class Chromosome(ABC):
    """Abstract class for Chromosome."""

    @abstractmethod
    def __init__(self, parameters: GeneticAlgoParameter):
        """Initialize Chromosome."""
        self.params = parameters

    @abstractmethod
    def get_fitness(self):
        """Get fitness of chromosome."""
        pass

    @abstractmethod
    def __str__(self):
        """Return string representation of chromosome."""
        pass

    def __eq__(self, other):
        """Return True if chromosome is equal to other."""
        if not isinstance(other, Chromosome):
            return NotImplemented
        return self.get_fitness() == other.get_fitness()

    @abstractmethod
    def __lt__(self, other):
        """Return True if chromosome is less than other."""
        if not isinstance(other, Chromosome):
            return NotImplemented
        return self.get_fitness() > other.get_fitness()
