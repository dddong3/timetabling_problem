from ..genetic_algo.parameter import GeneticAlgoParameter
from ..genetic_algo.select import Select
from ..genetic_algo.select import StrategyRegistry as SelectStrategyRegistry
from .chromosome import Chromosome

import random


@SelectStrategyRegistry.register("roulette")
class RouletteSelect(Select):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def select_one(self, chromosomes: list[Chromosome], probabilities: list[float]) -> Chromosome:
        selected = None
        r = random.random()
        for i, chromosome in enumerate(chromosomes):
            if r < probabilities[i]:
                selected = chromosome
                break
            r -= probabilities[i]

        return selected

    def select(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        total_fitness = sum(chromosome.fitness for chromosome in chromosomes)
        probabilities = [chromosome.fitness / total_fitness for chromosome in chromosomes]
        new_chromosomes = []
        for _ in range(self.params.population_size):
            selected = self.select_one(chromosomes, probabilities)
            new_chromosomes.append(selected)

        return new_chromosomes
