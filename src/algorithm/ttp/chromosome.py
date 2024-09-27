import copy
import random

from src.algorithm.genetic_algo.chromosome import Chromosome as GeneticAlgoChromosome
from src.algorithm.genetic_algo.chromosome import ChromosomeRegistry
from src.algorithm.genetic_algo.parameter import GeneticAlgoParameter
from src.algorithm.models.curriculum import Curriculum
from src.algorithm.services.fitness.app import FitnessService
from src.algorithm.services.school_curriculum import SchoolCurriculumService
from src.algorithm.models.classroom import Classroom

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

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
        curruculum.session = random.choice(SESSION_TABLE)
        curriculums.append(curruculum)
    return curriculums


def copy_curriculum() -> list[Curriculum]:
    return copy.deepcopy(school_curruculum_template)

class CurriculumView:
    def __init__(self, snapshot: "CurriculumSnapshot"):
        self.snapshot = snapshot

    def filter_time(self, start: str):
        """
        :param start: "week-session" or "week/session (e.g. 1-1 or 1/1)"
        :param end: "week-session" or "week/session (e.g. 1-1 or 1/1)"
        :return: CurriculumView
        """
        
        if "-" in start:
            start_week, start_session = start.split("-")
        else:
            start_week, start_session = start.split("/")

        start_week, start_session = int(start_week), int(start_session)

        self.filter_time_view = copy.deepcopy(self.snapshot.time_view)
        # print(self.filter_time_view)
        # print(start_week, start_session, end_week, end_session)
        # self.filter_time_view = [
        #     [self.filter_time_view[week][session] for session in range(start_session, end_session + 1)]
        #     for week in range(start_week - 1, end_week)
        # ]
        # self.filter_time_view = {week: {session: self.filter_time_view[week][session] for session in range(start_session, len(self.filter_time_view[week]))} for week in range(start_week, 5)}
        self.filter_time_view = self.filter_time_view[start_week][start_session]

        return self
    
    def get_teacher(self):
        teachers = []
        # for week in self.filter_time_view:
        #     for session in week:
        #         for course in session:
        #             teachers.append(course["teacher"])
        for course in self.filter_time_view:
            teachers.append(course["teacher"])

        return teachers
    
    def get_classroom(self):
        classrooms = []
        # for week in self.filter_time_view:
        #     for session in week:
        #         for course in session:
        #             print(course)
        #             classrooms.append(course["classroom"])

        for course in self.filter_time_view:
            classrooms.append(course["classroom"])

        return classrooms
    
    # def get_grade(self):
    #     grades = []
    #     for course in self.filter_time_view:
    #         grades.append(course["grade"])
    #     return grades

    def get_course_type(self, grade):
        course_types = []
        for course in self.filter_time_view:
            if course["grade"] == grade:
                course_types.append(course["course_type"])
        return course_types


class CurriculumSnapshot:
    def __init__(self, curriculums):
        # self.time_view = [[[] for _ in range(len(SESSION_TABLE))] for _ in range(5)]
        self.time_view = {week: {session: [] for session in SESSION_TABLE} for week in range(1, 6)}

        for curriculum in curriculums:
            for s in range(curriculum.session):
                # self.time_view[curriculum.week - 1][(SESSION_TABLE.index(curriculum.session) + s) % len(self.time_view[curriculum.week - 1])].append(
                #     {
                #         "course_key": curriculum.course_key,
                #         "classroom": curriculum.classroom,
                #         "teacher": curriculum.teachers,
                #     }
                # )
                session_idx = (SESSION_TABLE.index(curriculum.session) + s) % len(SESSION_TABLE)
                session = SESSION_TABLE[session_idx]
                self.time_view[curriculum.week][session].append( 
                    {
                        "course_key": curriculum.course_key,
                        "classroom": curriculum.classroom,
                        "teacher": curriculum.teachers,
                        "grade": curriculum.grade,
                        "course_type": curriculum.course_type
                    }

                )


    def get_view(self):
        return CurriculumView(self)


@ChromosomeRegistry.register("TTP")
class Chromosome(GeneticAlgoChromosome):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)
        # self._curriculums: list[Curriculum] = copy_curriculum()
        self._curriculums: list[Curriculum] = random_curriculum()
        self.fitness = self.get_fitness()

    @property
    def curriculums(self):
        return self._curriculums

    @curriculums.setter
    def curriculums(self, value):
        self._curriculums = value
        # self.fitness = self.get_fitness()

    def find_by_course_key(self, course_key: str) -> Curriculum:
        for curriculum in self.curriculums:
            if curriculum.course_key == course_key:
                return curriculum
        return None

    def set_classroom(self, course_key: str, classroom: Classroom):
        for curriculum in self.curriculums:
            if curriculum.course_key == course_key:
                curriculum.classroom = classroom

    def set_time(self, course_key: str, time: str):
        """
        :param course_key: course key
        :param time: "week-session" or "week/session (e.g. 1-1 or 1/1)"
        """
        if "-" in time:
            week, session = time.split("-")
        else:
            week, session = time.split("/")
        week, session = int(week), int(session)

        for curriculum in self.curriculums:
            if curriculum.course_key == course_key:
                curriculum.week = week
                curriculum.session = session

    def get_snapshot(self):
        return CurriculumSnapshot(self.curriculums)

    def get_fitness(self):
        return fitness_service.get_fitness(self.curriculums)
    
    def get_record(self):
        return fitness_service.record(self.curriculums)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return str(self.fitness)

    def __lt__(self, other):
        return self.fitness < other.fitness
