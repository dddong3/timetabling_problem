import time
import json
import random
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

    def run(self: object) -> None:
        self.chromosome = [self.generate_chromosome() for _ in range(self.population_size)]
        self.fitness = [self.compute_fitness(chromosome) for chromosome in self.chromosome]
        self.update_best_fitness()
        for _ in range(self.livecycle):
            self.cross_over()
            self.update_best_fitness()
            self.mutation()
            self.update_best_fitness()
            self.selection()

    def update_best_fitness(self: object) -> None:
        self.best_fitness = max(self.fitness)
        self.best_chromosome = self.chromosome[self.fitness.index(self.best_fitness)]
    
    def cross_over(self: object) -> None:
        self.chromosome.extend([self.generate_chromosome() for _ in range(self.population_size)])
        self.fitness.extend([self.compute_fitness(chromosome) for chromosome in self.chromosome[self.population_size:]])

    def mutation(self: object) -> None:
        pass

    def selection(self: object) -> None:
        self.chromosome = [chromosome for _, chromosome in sorted(zip(self.fitness, self.chromosome), reverse=True)]
        self.fitness = sorted(self.fitness, reverse=True)
        self.chromosome = self.chromosome[:self.population_size]
        self.fitness = self.fitness[:self.population_size]

    def output_chromosome(self: object) -> None:
        fileName = f'chromosome_{self.best_fitness}_{time.strftime("%m%d.%H%M", time.localtime())}.json'
        json.dump(self.best_chromosome, open(fileName, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

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
    