from ..genetic_algo.crossover import Crossover
from ..genetic_algo.crossover import StrategyRegistry as CrossoverStrategyRegistry
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome


@CrossoverStrategyRegistry.register("pmx")
class PMXCrossover(Crossover):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def crossover(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        return chromosomes
