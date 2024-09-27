import copy
import multiprocessing
from multiprocessing import Queue
from typing import List, NoReturn
from matplotlib import pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from .chromosome import Chromosome, ChromosomeRegistry
from .crossover import StrategyRegistry as CrossoverStrategyRegistry
from .mutate import StrategyRegistry as MutateStrategyRegistry
from .parameter import GeneticAlgoParameter
from .select import StrategyRegistry as SelectStrategyRegistry

plt.switch_backend('Agg') 

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
        self.best_chromosome: Chromosome = copy.deepcopy(self.chromosome_list[0])
        best_record = [self.best_chromosome.fitness]
        for _ in range(self.params.max_generation):
            self.chromosome_list = self.SELECT_STRATEGY.select(self.chromosome_list)
            self.chromosome_list = self.CROSSOVER_STRATEGY.crossover(
                self.chromosome_list
            )
            self.chromosome_list = self.MUTATE_STRATEGY.mutate(self.chromosome_list)
            # [chromosome.get_fitness() for chromosome in self.chromosome_list]

            with ThreadPoolExecutor() as executor:
                fitness_values = list(executor.map(self.evaluate_fitness, self.chromosome_list))

            # self.best_chromosome = max(self.chromosome_list)
            # self.best_chromosome = copy.deepcopy(max(self.chromosome_list))

            for chromosome in self.chromosome_list:
                if chromosome.fitness > self.best_chromosome.fitness:
                    self.best_chromosome = copy.deepcopy(chromosome)

            best_record.append(self.best_chromosome.fitness)
            print(f"Generation: {_}, Best Fitness: {self.best_chromosome.fitness}")

        plt.plot(best_record)
        plt.savefig("data/results/fitness.png")

        return self.best_chromosome

    def  run_app(self) -> List[Chromosome]:
        with multiprocessing.Pool() as pool:
            results = pool.map(self.run_ga, range(self.params.loops))
        # return [self.run_ga() for _ in range(self.params.loops)]
        return results
    
    def evaluate_fitness(self, chromosome: Chromosome) -> Chromosome:
        chromosome.fitness = chromosome.get_fitness()
        return chromosome
