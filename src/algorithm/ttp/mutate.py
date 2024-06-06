import random

from ..genetic_algo.mutate import Mutate
from ..genetic_algo.mutate import StrategyRegistry as MutateStrategyRegistry
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome


@MutateStrategyRegistry.register("swap_small")
class SwapMutate(Mutate):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def swap_small_class(self, idx: int, chromosome: Chromosome):
        curriculums_size = len(chromosome.curriculums)
        curriculums = chromosome.curriculums

        idx2 = random.randint(0, curriculums_size - 1)
        curriculums[idx].classroom, curriculums[idx2].classroom = (
            curriculums[idx2].classroom,
            curriculums[idx].classroom,
        )

        return chromosome

    def mutate(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        for chromosome_idx in range(len(chromosomes)):
            for curriculum_idx in range(len(chromosomes[chromosome_idx].curriculums)):
                if random.random() > self.params.mutation_rate:
                    continue

                chromosomes[chromosome_idx] = self.swap_small_class(
                    curriculum_idx, chromosomes[chromosome_idx]
                )
            # if random.random() > self.params.mutation_rate:
            #     continue

            # chromosome = self.swap_small_class(curriculum_idx, chromosome)

        return chromosomes
