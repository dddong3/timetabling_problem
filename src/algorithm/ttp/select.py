from ..genetic_algo.parameter import GeneticAlgoParameter
from ..genetic_algo.select import Select
from ..genetic_algo.select import StrategyRegistry as SelectStrategyRegistry
from .chromosome import Chromosome


@SelectStrategyRegistry.register("roulette")
class RouletteSelect(Select):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def select(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        return chromosomes
