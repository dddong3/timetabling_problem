import json
import time

from src.algorithm.services.curriculum import CurriculumService

from ..genetic_algo.app import GeneticAlgoApp
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome
from .crossover import *
from .mutate import *
from .select import *
from ..services.fitness.app import FitnessService

curriculum_service = CurriculumService()
fitness_service = FitnessService()

ga_params = GeneticAlgoParameter(
    population_size=100,
    mutation_rate=0.5,
    crossover_rate=0.7,
    crossover_strategy="swap",
    mutate_strategy="resolve_conflict",
    select_strategy="roulette",
    max_generation=100,
    loops=5,
)


def run(**kwargs) -> Chromosome:
    # [setattr(ga_params, k, v) for k, v in kwargs.items() if hasattr(ga_params, k)]
    ga_params.population_size = kwargs.get("popu", 100)
    ga_params.max_generation = kwargs.get("live", 10)
    start_time = time.perf_counter()
    best_chromosome_list = GeneticAlgoApp(genetic_algo_parameter=ga_params).run_app()
    end_time = time.perf_counter()
    best_chromosome_list = sorted(best_chromosome_list, key=lambda x: x.fitness, reverse=True)
    print(best_chromosome_list)
    print(f"Time: {end_time - start_time} seconds")
    file_prefix = f'data/results/chromosome_{best_chromosome_list[0].fitness}_{time.strftime("%m%d%H%M", time.localtime())}'
    file_name = f'{file_prefix}.json'
    # file_name = f'data/results/chromosome_{best_chromosome_list[0].fitness}_{time.strftime("%m%d%H%M", time.localtime())}.json'
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(
            curriculum_service.convert_to_school_curriculum(
                best_chromosome_list[0].curriculums
            ),
            f,
            default=lambda x: x.__dict__,
            ensure_ascii=False,
            indent=4,
        )

    fitness_service.record_and_output(f'{file_prefix}_record.json',best_chromosome_list[0].curriculums)
    fitness_service.output_rule()


if __name__ == "__main__":
    run(live=20, popu=20)
