from .penalty import Penalty
from .bonus import Bonus
from typing import Any, Dict

class Fitness():
    START_WEEK, END_WEEK = 1, 5
    session_list = ['01', '02', '03', '04', '20', '05', '06', '07', '08', '09', '40', '50', '60', '70']

    def __init__(self):
        self.penalty = Penalty(self.session_list)
        self.bonus = Bonus(self.session_list)
        with open('fitness/fitness_weight.cfg', 'r') as f:
            self.fitness_weight =  {line.split('=')[0].strip(): int(line.split('=')[1]) for line in f.readlines()}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.compute_fitness(*args, **kwds)

    def compute_fitness(self, chromosome: list[dict]) -> dict:
        fitness = {
            'penalty': dict(),
            'bonus': dict()
        }

        fitness['bonus']['start_on_2_5'] = self.bonus.start_on_2_5(chromosome)
        fitness['penalty']['exceed_time'] = self.penalty.exceed_time(chromosome)
        fitness['penalty']['over_07'] = self.penalty.over_07(chromosome)
        fitness['penalty']['working_overtime'] = self.penalty.working_overtime(chromosome)

        for subdict in fitness:
            for key in fitness[subdict]:
                fitness[subdict][key] *= self.fitness_weight[key]

        return fitness

