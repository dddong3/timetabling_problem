import copy
import multiprocessing
from multiprocessing import Queue
from typing import List, NoReturn

from .chromosome import Chromosome, ChromosomeRegistry
from .crossover import StrategyRegistry as CrossoverStrategyRegistry
from .mutate import StrategyRegistry as MutateStrategyRegistry
from .parameter import GeneticAlgoParameter
from .select import StrategyRegistry as SelectStrategyRegistry


class GeneticAlgoApp:
    def __init__(
        self, *, genetic_algo_parameter: GeneticAlgoParameter, data: dict = None
    ):

        self.params = genetic_algo_parameter
        if data is None:
            data = {}
        self.data = data

        self.CHROMOSOME = ChromosomeRegistry.get_strategy(
            genetic_algo_parameter.chromosome_type
        )

        self.CROSSOVER_STRATEGY = CrossoverStrategyRegistry.get_strategy(
            genetic_algo_parameter.crossover_strategy
        )(parameters=genetic_algo_parameter, data=data.get("crossover", None))
        self.MUTATE_STRATEGY = MutateStrategyRegistry.get_strategy(
            genetic_algo_parameter.mutate_strategy
        )(parameters=genetic_algo_parameter, data=data.get("mutate", None))
        self.SELECT_STRATEGY = SelectStrategyRegistry.get_strategy(
            genetic_algo_parameter.select_strategy
        )(parameters=genetic_algo_parameter, data=data.get("select", None))

    def run_ga(self) -> Chromosome:
        self.chromosome_list: list[Chromosome] = [
            self.CHROMOSOME(
                parameters=self.params, data=self.data.get("chromosome", None)
            )
            for _ in range(self.params.population_size)
        ]
        self.best_chromosome: Chromosome = self.chromosome_list[0]

        for _ in range(self.params.max_generation):
            self.chromosome_list = self.SELECT_STRATEGY.select(self.chromosome_list)
            self.chromosome_list = self.CROSSOVER_STRATEGY.crossover(
                self.chromosome_list
            )
            self.chromosome_list = self.MUTATE_STRATEGY.mutate(self.chromosome_list)
            self.best_chromosome = min(self.chromosome_list)

        return self.best_chromosome

    def run_app(self) -> List[Chromosome]:
        return [self.run_ga() for _ in range(self.params.loops)]
