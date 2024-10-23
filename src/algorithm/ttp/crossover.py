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

        return chromosome1, chromosome2

    def swap_course(self, chromosome1: Chromosome, chromosome2: Chromosome):
        p1, p2 = chromosome1.curriculums, chromosome2.curriculums
        curriculums_size = len(p1)
        idxl, idxr = random.sample(range(curriculums_size), 2)
        p1[idxl:idxr], p2[idxl:idxr] = p2[idxl:idxr], p1[idxl:idxr]

        course_cnt_1 = {}
        course_cnt_2 = {}

        for i in range(len(p1)):
            course_key_1 = p1[i].course_key
            if course_key_1 in course_cnt_1:
                course_cnt_1[course_key_1] += 1
            else:
                course_cnt_1[course_key_1] = 1


        for i in range(len(p2)):
            course_key_2 = p2[i].course_key
            if course_key_2 in course_cnt_2:
                course_cnt_2[course_key_2] += 1
            else:
                course_cnt_2[course_key_2] = 1

        course_list_1 = list(filter(lambda x: course_cnt_1[x] > 1, course_cnt_1.keys()))
        course_list_2 = list(filter(lambda x: course_cnt_2[x] > 1, course_cnt_2.keys()))

        for i in range(len(course_list_1)):
            course_key_1 = course_list_1[i]
            course_key_2 = course_list_2[i]
            p1_idx = [j for j in range(len(p1)) if p1[j].course_key == course_key_1][0]
            p2_idx = [j for j in range(len(p2)) if p2[j].course_key == course_key_2][0]

            # p1[p1_idx].course_key = course_key_2
            # p1[p1_idx].classroom = p2[p2_idx].classroom
            # p1[p1_idx].teachers = p2[p2_idx].teachers
            # p1[p1_idx].class_size = p2[p2_idx].class_size
            # p1[p1_idx].class_type = p2[p2_idx].class_type
            # p1[p1_idx].grade = p2[p2_idx].grade
            # p1[p1_idx].course_type = p2[p2_idx].course_type

            # p1[p1_idx].course_key, p2[p2_idx].course_key = p2[p2_idx].course_key, p1[p1_idx].course_key
            # p1[p1_idx].classroom, p2[p2_idx].classroom = p2[p2_idx].classroom, p1[p1_idx].classroom
            # p1[p1_idx].teachers, p2[p2_idx].teachers = p2[p2_idx].teachers, p1[p1_idx].teachers
            # p1[p1_idx].class_size, p2[p2_idx].class_size = p2[p2_idx].class_size, p1[p1_idx].class_size
            # p1[p1_idx].class_type, p2[p2_idx].class_type = p2[p2_idx].class_type, p1[p1_idx].class_type
            # p1[p1_idx].grade, p2[p2_idx].grade = p2[p2_idx].grade, p1[p1_idx].grade
            # p1[p1_idx].course_type, p2[p2_idx].course_type = p2[p2_idx].course_type, p1[p1_idx].course_type
            p1[p1_idx].week, p2[p2_idx].week = p2[p2_idx].week, p1[p1_idx].week
            p1[p1_idx].session, p2[p2_idx].session = p2[p2_idx].session, p1[p1_idx].session
            p1[p1_idx].classroom, p2[p2_idx].classroom = p2[p2_idx].classroom, p1[p1_idx].classroom



        return chromosome1, chromosome2


    def swap_big(self, chromosome1: Chromosome, chromosome2: Chromosome):
        # return self.swap_classroom(chromosome1, chromosome2)
        return self.swap_course(chromosome1, chromosome2)

    def crossover(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        for i in range(0, len(chromosomes), 2):
            if random.random() < self.params.crossover_rate:
                c1, c2 = self.swap_big(chromosomes[i], chromosomes[i + 1])
                chromosomes[i] = c1
                chromosomes[i + 1] = c2

        return chromosomes

@CrossoverStrategyRegistry.register("skip")
class SkipCrossover(Crossover):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def crossover(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        return chromosomes
    
@CrossoverStrategyRegistry.register("swap")
class SwapCrossover(Crossover):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def swap(self, chromosome1: Chromosome, chromosome2: Chromosome):
        # return self.swap_classroom(chromosome1, chromosome2)
        p1, p2 = chromosome1.curriculums, chromosome2.curriculums
        curriculums_size = len(p1)
        idxl, idxr = random.sample(range(curriculums_size), 2)
        p1[idxl:idxr], p2[idxl:idxr] = p2[idxl:idxr], p1[idxl:idxr]


    def crossover(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        for i in range(0, len(chromosomes), 2):
            if random.random() < self.params.crossover_rate:
                self.swap(chromosomes[i], chromosomes[i + 1])

        return chromosomes