import copy
import random

from src.algorithm.genetic_algo.chromosome import Chromosome as GeneticAlgoChromosome
from src.algorithm.genetic_algo.chromosome import ChromosomeRegistry
from src.algorithm.genetic_algo.parameter import GeneticAlgoParameter
from src.algorithm.models.curriculum import Curriculum
from src.algorithm.services.fitness.app import FitnessService
from src.algorithm.services.school_curriculum import SchoolCurriculumService
from src.algorithm.models.classroom import Classroom
from src.algorithm.services.custom_rule import CustomRuleService
SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

fitness_service = FitnessService()
school_curriculum_service = SchoolCurriculumService()
school_curruculum_template = school_curriculum_service.convert_to_curriculum(
    school_curriculum_service.school_curriculums
)
custom_rule_service = CustomRuleService()

def check_classroom_with_curriculum(curriculum_class_size: int, curriculum_class_type: str, classroom: Classroom) -> bool:
    if classroom.size < curriculum_class_size:
        return False
    
    if curriculum_class_type[0] == "0":
        return True
    
    if curriculum_class_type == "1" and classroom.type == "1":
        return True
    
    if curriculum_class_type[0] == "2" and classroom.type[0] == "2":
        if curriculum_class_type[2] == "0":
            return True
        return curriculum_class_type[2] == classroom.type[2]
    
    # raise ValueError(f"Invalid class size {curriculum_class_size} or class type {curriculum_class_type} or classroom {classroom.size} {classroom.type}")
    return False

def random_classroom_with_curriculum(curriculum: Curriculum) -> Classroom:
    classrooms = school_curriculum_service.classrooms
    
    while True:
        classroom = random.choice(classrooms)
        if check_classroom_with_curriculum(curriculum.class_size, curriculum.class_type, classroom):
            # print(f"random classroom {classroom.id}")
            return classroom
        
        # print(f"random {curriculum.class_size} {curriculum.class_type} {classroom.size} {classroom.type}")

    return None

def random_curriculum() -> list[Curriculum]:
    # classrooms = school_curriculum_service.classrooms
    # random.shuffle(classrooms)
    curriculums = []
    for curruculum in school_curruculum_template:
        # curruculum.classroom = random.choice(classrooms)
        if custom_rule_service.check_course_key_in_rule(curruculum.course_key):
            time = custom_rule_service.get_requirement_time_by_course_key(curruculum.course_key)
            curruculum.week, curruculum.session = time.split("/")
            curruculum.week = int(curruculum.week)
            curruculum.session = int(curruculum.session)
            curruculum.classroom = random_classroom_with_curriculum(curruculum)
        else:
            curruculum.classroom = random_classroom_with_curriculum(curruculum)
            curruculum.week = random.randint(1, 5)
            end_idx = len(SESSION_TABLE) - curruculum.session_length  - 1
            # curruculum.session = random.choice(SESSION_TABLE[])
            # print(curruculum.session_length, len(SESSION_TABLE), end_idx)
            session_list = None
            if curruculum.session_length == 1:
                session_list = [1]
            elif curruculum.session_length == 2:
                session_list = [1, 3, 5, 7]
            elif curruculum.session_length == 3:
                session_list = [2, 5]
            # curruculum.session = random.choice(SESSION_TABLE[:end_idx])
            curruculum.session = random.choice(session_list)
        curriculums.append(curruculum)


        # curriculums.append(copy.deepcopy(curruculum))
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

        # self.filter_time_view = copy.deepcopy(self.snapshot.time_view)
        self.filter_time_view = self.snapshot.time_view[start_week][start_session]
        # self.filter_time_view = self.filter_time_view

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
        # classrooms = set()
        # for week in self.filter_time_view:
        #     for session in week:
        #         for course in session:
        #             print(course)
        #             classrooms.append(course["classroom"])

        for course in self.filter_time_view:
            classrooms.append(course["classroom"])
            # classrooms.add(course["classroom"])

        return classrooms
    
    def check_conflict_classroom(self, week, session, classroom):
        # class_list = []
        for course in self.filter_time_view:
            if course["classroom"] == classroom:
                # class_list.append(course)


            # print(class_list)
                return True
        # print(f"{classroom} {week} {session}")
        return False
    
    def check_conflict_teacher(self, week, session, teacher):
        # teacher_time_dict = {}
        # session_idx = SESSION_TABLE.index(session)
        # for s in range(1):
        #     if teacher_time_dict.get(teacher) is None:
        #         teacher_time_dict[teacher] = {}
        #     time = str(SESSION_TABLE[(session_idx + s)]) + str(week)

        #     if teacher_time_dict[teacher].get(time, 0) > 0:
        #         return True
        
        #     teacher_time_dict[teacher][time] = 1
        for course in self.filter_time_view:
            # print(course["teacher"], teacher)
            # if course["teacher"] == teacher:
            if school_curriculum_service.check_teacher(course["teacher"], teacher):
                return True
        return False
    
    def check_conflict_course_type(self, week, session, course_class, course_type, grade):
        for course in self.filter_time_view:
            if course["course_class"] == course_class:
                return True
            if course["grade"] == grade and ((course["course_type"] == "必修" and course_type == "選修") or (course["course_type"] == "選修" and course_type == "必修")):
                return True
        return False

    # def get_grade(self):
    #     grades = []
    #     for course in self.filter_time_view:
    #         grades.append(course["grade"])
    #     return grades

    def get_course_type(self, grade):
        course_types = set()
        for course in self.filter_time_view:
            if course["grade"] == grade:
                # course_types.append(course["course_type"])
                # print(course)
                course_types.add(course["course_type"])

        return course_types


class CurriculumSnapshot:
    def __init__(self, curriculums):
        # self.time_view = [[[] for _ in range(len(SESSION_TABLE))] for _ in range(5)]
        self.time_view = {week: {session: [] for session in SESSION_TABLE} for week in range(1, 6)}

        for curriculum in curriculums:
            for s in range(curriculum.session_length):
                # self.time_view[curriculum.week - 1][(SESSION_TABLE.index(curriculum.session) + s) % len(self.time_view[curriculum.week - 1])].append(
                #     {
                #         "course_key": curriculum.course_key,
                #         "classroom": curriculum.classroom,
                #         "teacher": curriculum.teachers,
                #     }
                # )
                # print(curriculum)
                # print(curriculum.week, curriculum.session, s)

                session_idx = (SESSION_TABLE.index(curriculum.session) + s) #% len(SESSION_TABLE)
                session = SESSION_TABLE[session_idx]

                self.time_view[curriculum.week][session].append( 
                    {
                        "course_key": curriculum.course_key,
                        "classroom": curriculum.classroom,
                        "teacher": curriculum.teachers,
                        "grade": curriculum.grade,
                        "course_type": curriculum.course_type,
                        "course_class": curriculum.course_class,
                    }

                )


    def get_view(self):
        return CurriculumView(self)


@ChromosomeRegistry.register("TTP")
class Chromosome(GeneticAlgoChromosome):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)
        # self._curriculums: list[Curriculum] = copy_curriculum()
        # self.fitness = -25000000
        # while -300000 > self.fitness:
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
    
    def find_by_time_classroom(self, week: int, session: int, classroom: Classroom) -> Curriculum:
        for curriculum in self.curriculums:
            if curriculum.week == week and curriculum.session == session and curriculum.classroom == classroom:
                return curriculum
        return None

    def set_classroom(self, course_key: str, classroom: Classroom):
        # for curriculum in self.curriculums:
        #     if curriculum.course_key == course_key:
        #         curriculum.classroom = classroom
        curriculum_idx = self.curriculums.index(self.find_by_course_key(course_key))
        self.curriculums[curriculum_idx].classroom = classroom


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

        # for curriculum in self.curriculums:
        #     if curriculum.course_key == course_key:
        #         curriculum.week = week
        #         curriculum.session = session
        curriculum_idx = self.curriculums.index(self.find_by_course_key(course_key))
        self.curriculums[curriculum_idx].week = week
        self.curriculums[curriculum_idx].session = session

    def get_snapshot(self):
        # return CurriculumSnapshot(self.curriculums)
        return CurriculumSnapshot(copy.deepcopy(self.curriculums))

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
