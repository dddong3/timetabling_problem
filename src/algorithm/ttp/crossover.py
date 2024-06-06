import random

from ..genetic_algo.crossover import Crossover
from ..genetic_algo.crossover import StrategyRegistry as CrossoverStrategyRegistry
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome


@CrossoverStrategyRegistry.register("swap_big")
class SwapBigCrossover(Crossover):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def swap_classroom(self, chromosome1: Chromosome, chromosome2: Chromosome):
        p1, p2 = chromosome1.curriculums, chromosome2.curriculums
        curriculums_size = len(p1)
        class1_idx, class2_idx = random.sample(range(curriculums_size), 2)
        class1, class2 = map(lambda x: x.classroom, [p1[class1_idx], p2[class2_idx]])
        for i in range(curriculums_size):
            if p1[i].classroom == class1 or p1[i].classroom == class2:
                p1[i].classroom = class2 if p1[i].classroom == class1 else class1
            elif p2[i].classroom == class1 or p2[i].classroom == class2:
                p2[i].classroom = class2 if p2[i].classroom == class1 else class1

        

    def swap_big(self, chromosome1: Chromosome, chromosome2: Chromosome):
        return self.swap_classroom(chromosome1, chromosome2)

    def crossover(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        for i in range(0, len(chromosomes), 2):
            if random.random() < self.params.crossover_rate:
                self.swap_big(chromosomes[i], chromosomes[i + 1])

        return chromosomes
