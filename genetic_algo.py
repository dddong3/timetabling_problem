import time
import json
import random
from typing import Any
from fitness import Fitness

class GeniticAlgoithm:
    START_WEEK, END_WEEK = Fitness.START_WEEK, Fitness.END_WEEK
    session_list = Fitness.session_list
    livecycle = None
    gene_list = None
    class_list = None
    class_detail = None
    population_size = None
    def __init__(self: object) -> None:
        assert(self.START_WEEK <= self.END_WEEK)
        assert(self.population_size is not None)
        assert(self.livecycle is not None)
        assert(self.gene_list is not None)
        assert(self.class_detail is not None)
        assert(self.class_list is not None)
        assert(self.session_list is not None)

        self.chromosome = None
        self.fitness = None
        self.fitness_rcd = None
        self.compute_fitness = Fitness()
        self.best_fitness = None
        self.best_chromosome = None
        self.run()

    @classmethod
    def init(cls, courseFileName: str, classFileName: str, *, popu: int, live: int) -> None:
        cls.population_size = popu
        cls.livecycle = live
        cls.gene_list = GeniticAlgoithm.get_json(courseFileName)
        cls.class_detail = GeniticAlgoithm.get_json(classFileName)
        cls.class_list = list(cls.class_detail.keys())

    def __lt__(self: object, other: object) -> bool:
        return self.best_fitness < other.best_fitness

    def get_fitness(self: object) -> list[int]:
        return [sum(subdict['penalty'].values()) + sum(subdict['bonus'].values())  for subdict in self.fitness_rcd]

    def run(self: object) -> None:
        self.chromosome = [self.generate_chromosome() for _ in range(self.population_size)]
        self.fitness_rcd = [self.compute_fitness(chromosome) for chromosome in self.chromosome]
        self.fitness = self.get_fitness()
        self.update_best_fitness()
        for _ in range(self.livecycle):
            self.cross_over()
            self.mutation()
            self.selection()
            self.update_best_fitness()
        print(self.fitness_rcd[self.fitness.index(self.best_fitness)])

    def update_best_fitness(self: object) -> None:
        self.fitness = self.get_fitness()
        self.best_fitness = max(self.fitness)
        self.best_chromosome = self.chromosome[self.fitness.index(self.best_fitness)]
    
    def cross_over(self: object) -> None:
        child = [self.generate_chromosome() for _ in range(self.population_size)]
        child_fitness = [self.compute_fitness(chromosome) for chromosome in child]
        self.chromosome.extend(child)
        self.fitness_rcd.extend(child_fitness)

    def mutation(self: object) -> None:
        pass

    def selection(self: object) -> None:
        # print(self.fitness)
        self.chromosome = [chromosome for _, chromosome in sorted(zip(self.fitness, self.chromosome), reverse=True)]
        self.fitness = sorted(self.fitness, reverse=True)
        self.chromosome = self.chromosome[:self.population_size]
        self.fitness = self.fitness[:self.population_size]
        self.fitness_rcd = self.fitness_rcd[:self.population_size]

    def output_chromosome(self: object) -> None:
        chromosome = []
        for course in self.best_chromosome:
            for i in range(course['session_length']):
                course['session'] = self.session_list[(self.session_list.index(course['session']) + (1 if i > 0 else 0)) % len(self.session_list)]
                chromosome.append(course.copy())

        fileName = f'chromosome_{self.best_fitness}_{time.strftime("%m%d%H%M", time.localtime())}.json'
        json.dump(chromosome, open(fileName, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    @staticmethod
    def get_json(fileName: str) -> dict:
        return json.load(open(fileName, 'r', encoding='utf-8'))

    def generate_chromosome(self: object) -> list[list[dict]]:
        
        chromosome = self.gene_list.copy()
        for course in chromosome:
            course['week'] = random.randint(self.START_WEEK, self.END_WEEK)
            course['session'] = random.choice(self.session_list)
            course['classroom'] = random.choice(self.class_list)
        return chromosome
    