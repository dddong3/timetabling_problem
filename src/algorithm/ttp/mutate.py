from ..genetic_algo.mutate import Mutate
from ..genetic_algo.mutate import StrategyRegistry as MutateStrategyRegistry
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome


@MutateStrategyRegistry.register("swap")
class SwapMutate(Mutate):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def mutate(self, chromosome: Chromosome) -> Chromosome:
        return chromosome
