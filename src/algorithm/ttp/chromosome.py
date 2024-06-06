import copy
import random

from src.algorithm.genetic_algo.chromosome import Chromosome as GeneticAlgoChromosome
from src.algorithm.genetic_algo.chromosome import ChromosomeRegistry
from src.algorithm.genetic_algo.parameter import GeneticAlgoParameter
from src.algorithm.models.curriculum import Curriculum
from src.algorithm.services.fitness import FitnessService
from src.algorithm.services.school_curriculum import SchoolCurriculumService

fitness_service = FitnessService()
school_curriculum_service = SchoolCurriculumService()
school_curruculum_template = school_curriculum_service.convert_to_curriculum(
    school_curriculum_service.school_curriculums
)


def random_curriculum() -> list[Curriculum]:
    classrooms = school_curriculum_service.classrooms
    random.shuffle(classrooms)
    curriculums = []
    for curruculum, classroom in zip(school_curruculum_template, classrooms):
        curruculum.classroom = classroom
        curruculum.week = random.randint(1, 5)
        curriculums.append(curruculum)
    return curriculums


def copy_curriculum() -> list[Curriculum]:
    return copy.deepcopy(school_curruculum_template)


@ChromosomeRegistry.register("TTP")
class Chromosome(GeneticAlgoChromosome):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)
        self._curriculums: list[Curriculum] = copy_curriculum()
        self.fitness = self.get_fitness()

    @property
    def curriculums(self):
        return self._curriculums

    @curriculums.setter
    def curriculums(self, value):
        self._curriculums = value
        # self.fitness = self.get_fitness()

    def get_fitness(self):
        return fitness_service.get_fitness(self.curriculums)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return str(self.fitness)

    def __lt__(self, other):
        return self.fitness < other.fitness
