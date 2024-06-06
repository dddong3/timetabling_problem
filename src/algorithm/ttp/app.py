import json
import time

from src.algorithm.services.curriculum import CurriculumService

from ..genetic_algo.app import GeneticAlgoApp
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome
from .crossover import *
from .mutate import *
from .select import *

curriculum_service = CurriculumService()

ga_params = GeneticAlgoParameter(
    population_size=100,
    mutation_rate=0.01,
    crossover_rate=0.7,
    crossover_strategy="swap_big",
    mutate_strategy="swap_small",
    select_strategy="roulette",
    max_generation=100,
    loops=10,
)


def run(**kwargs) -> Chromosome:
    [setattr(ga_params, k, v) for k, v in kwargs.items() if hasattr(ga_params, k)]
    best_chromosome_list = GeneticAlgoApp(genetic_algo_parameter=ga_params).run_app()
    print(best_chromosome_list)
    file_name = f'data/results/chromosome_{best_chromosome_list[0].fitness}_{time.strftime("%m%d%H%M", time.localtime())}.json'
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


if __name__ == "__main__":
    run(live=20, popu=20)
