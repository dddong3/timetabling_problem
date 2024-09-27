import random

from ..genetic_algo.mutate import Mutate
from ..genetic_algo.mutate import StrategyRegistry as MutateStrategyRegistry
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

@MutateStrategyRegistry.register("swap_small")
class SwapMutate(Mutate):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def swap_small_class(self, idx: int, chromosome: Chromosome):
        curriculums_size = len(chromosome.curriculums)
        curriculums = chromosome.curriculums

        idx2 = random.randint(0, curriculums_size - 1)
        curriculums[idx].classroom, curriculums[idx2].classroom = (
            curriculums[idx2].classroom,
            curriculums[idx].classroom,
        )

        return chromosome

    def mutate(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        for chromosome_idx in range(len(chromosomes)):
            for curriculum_idx in range(len(chromosomes[chromosome_idx].curriculums)):
                if random.random() > self.params.mutation_rate:
                    continue

                chromosomes[chromosome_idx] = self.swap_small_class(
                    curriculum_idx, chromosomes[chromosome_idx]
                )
            # if random.random() > self.params.mutation_rate:
            #     continue

            # chromosome = self.swap_small_class(curriculum_idx, chromosome)

        return chromosomes


@MutateStrategyRegistry.register("skip")
class SkipMutate(Mutate):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def mutate(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        return chromosomes
    

import random
from src.algorithm.services.school_curriculum import SchoolCurriculumService

school_curriculum_service = SchoolCurriculumService()
all_classrooms = school_curriculum_service.classrooms #notice Classroom  can't be change
all_session = [f'{week}/{session}' for week in range(1, 6) for session in SESSION_TABLE]

@MutateStrategyRegistry.register("resolve_conflict")
class ResolveConflictMutate(Mutate):
    def __init__(self, parameters: GeneticAlgoParameter, data: dict = None):
        super().__init__(parameters)

    def mutate(self, chromosomes: list[Chromosome]) -> list[Chromosome]:
        for chromosome in chromosomes:
            if random.random() > self.params.mutation_rate:
                continue
            chromosome = self.resolve_conflict(chromosome)
        return chromosomes
    
    def resolve_conflict(self, chromosome: Chromosome):
        conflict_record = self.get_conflict_record(chromosome)
        conflict_record.sort(key=lambda x: x["weight"])
        if len(conflict_record) == 0:
            return chromosome
        # conflict_record = sorted(conflict_record, key=lambda x: x["weight"])
        conflict_record = list(filter(lambda x: x["weight"] == conflict_record[0]["weight"], conflict_record))

        conflict = random.choice(conflict_record)

        # print(f"Conflict: {conflict}")

        match conflict["rule"]:
            case "ConflictClassroom":
                chromosome = self.solve_class_conflict(chromosome, conflict)

            case "ConflictTeacher":
                chromosome = self.solve_teacher_conflict(chromosome, conflict)

            case "over_70":
                chromosome = self.solve_over_70(chromosome, conflict)
            
            case "no_20":
                chromosome = self.solve_over_70(chromosome, conflict)

            case "conflict_grade_course":
                chromosome = self.solve_over_70(chromosome, conflict)

            case _:
                pass
                # raise NotImplementedError(f"Conflict rule {conflict['rule']} is not implemented")
            
        return chromosome

    def get_conflict_record(self, chromosome: Chromosome):
        chromosome_record = chromosome.get_record()
        chromosome_record_expand = []

        for course in chromosome_record:
            for fitness in course["fitness"]:
                chromosome_record_expand.extend(
                    {
                        "course_key": course["course_key"],
                        "rule": fitness["rule"],
                        "weight": fitness["weight"],
                    }
                    for _ in range(fitness["count"])
                )
        return chromosome_record_expand
    

    def solve_class_conflict(self, chromosome: Chromosome, conflict: dict):
        course_key = conflict["course_key"]
        curriculum = chromosome.find_by_course_key(course_key)
        classroom = curriculum.classroom
        teacher = curriculum.teachers
        chromosome_snapshot = chromosome.get_snapshot()
        chromosome_view = chromosome_snapshot.get_view()
        
        # for week in range(1, 6):
        #     for session in range(len(SESSION_TABLE) - curriculum.session_length + 1):
        #         if self.check_conflict(chromosome_view, classroom, teacher, week, session, curriculum.session_length):
        #             continue
        #         chromosome.set_time(course_key, f'{week}/{SESSION_TABLE[session]}')

        #         #TODO: Set classroom

        random.shuffle(all_classrooms)

        for classroom in all_classrooms:
                if self.check_conflict(chromosome_view, classroom, teacher, curriculum.week, SESSION_TABLE.index(curriculum.session), curriculum.session_length, curriculum.grade, curriculum.course_type):
                    continue
                chromosome.set_classroom(course_key, classroom)
                return chromosome
        # print(f"Cannot resolve conflict: {course_key}")

        random.shuffle(all_session)

        for session in all_session:
            week, session = session.split('/')
            if self.check_conflict(chromosome_view, classroom, teacher, int(week), SESSION_TABLE.index(int(session)), curriculum.session_length, curriculum.grade, curriculum.course_type):
                continue
            chromosome.set_time(course_key, f'{week}/{session}')
            return chromosome

        return chromosome
    
    def solve_teacher_conflict(self, chromosome: Chromosome, conflict: dict):
        course_key = conflict["course_key"]
        curriculum = chromosome.find_by_course_key(course_key)
        classroom = curriculum.classroom
        teacher = curriculum.teachers
        chromosome_snapshot = chromosome.get_snapshot()
        chromosome_view = chromosome_snapshot.get_view()

        # for week in range(1, 6):
        #     for session in range(len(SESSION_TABLE) - curriculum.session_length + 1):
        #         if self.check_conflict(chromosome_view, classroom, teacher, week, session, curriculum.session_length):
        #             continue
        #         chromosome.set_time(course_key, f'{week}/{SESSION_TABLE[session]}')
        #         # curriculum.week = week
        #         # curriculum.session = SESSION_TABLE[session:session + curriculum.session_length]
        #         # print(f"Resolve conflict: {course_key} to {week}/{SESSION_TABLE[session]}")
        #         return chromosome

        random.shuffle(all_session)

        for session in all_session:
            week, session = session.split('/')
            if self.check_conflict(chromosome_view, classroom, teacher, int(week), SESSION_TABLE.index(int(session)), curriculum.session_length, curriculum.grade, curriculum.course_type):
                continue
            chromosome.set_time(course_key, f'{week}/{session}')
            return chromosome
            
        # print(f"Cannot resolve conflict: {course_key}")
        return chromosome
    
    def solve_over_70(self, chromosome: Chromosome, conflict: dict):
        course_key = conflict["course_key"]
        curriculum = chromosome.find_by_course_key(course_key)
        classroom = curriculum.classroom
        teacher = curriculum.teachers
        chromosome_snapshot = chromosome.get_snapshot()
        chromosome_view = chromosome_snapshot.get_view()

        # for week in range(1, 6):
        #     for session in range(len(SESSION_TABLE) - curriculum.session_length + 1):
        #         if self.check_conflict(chromosome_view, classroom, teacher, week, session, curriculum.session_length):
        #             continue
        #         chromosome.set_time(course_key, f'{week}/{SESSION_TABLE[session]}')
        #         # curriculum.week = week
        #         # curriculum.session = SESSION_TABLE[session:session + curriculum.session_length]
        #         # print(f"Resolve conflict: {course_key} to {week}/{SESSION_TABLE[session]}")
        #         return chromosome

        random.shuffle(all_session)

        for session in all_session:
            week, session = session.split('/')
            if self.check_conflict(chromosome_view, classroom, teacher, int(week), SESSION_TABLE.index(int(session)), curriculum.session_length, curriculum.grade, curriculum.course_type):
                continue
            chromosome.set_time(course_key, f'{week}/{session}')
            return chromosome
            
        # print(f"Cannot resolve conflict: {course_key}")
        return chromosome
    
    def check_conflict(self, chromosome_view, classroom, teacher, week, session, session_length, grade, course_type):
        for s in range(session_length):
            if session + s >= len(SESSION_TABLE):
                return True
            if SESSION_TABLE[session + s] == 20:
                return True
            class_session = SESSION_TABLE[session + s]
            # class_session = SESSION_TABLE[(session + s) % len(SESSION_TABLE)]
            # print(f'Check conflict: {week}/{class_session} {classroom}')
            snapshot_classroom = chromosome_view.filter_time(f'{week}/{class_session}').get_classroom()
            snapshot_teacher = chromosome_view.filter_time(f'{week}/{class_session}').get_teacher()
            # snapshot_grade = chromosome_view.filter_time(f'{week}/{class_session}').get_grade()
            snapshot_course_type = chromosome_view.filter_time(f'{week}/{class_session}').get_course_type(grade)

            # if len(chromosome_view.filter_time(f'{week}/{class_session}').get_classroom()) > 0:
            # print(f"Check conflict: {week}/{class_session} {snapshot_classroom}")
            # print(f"Check conflict: {week}/{class_session} {classroom}")
            # print(f"Check conflict: {week}/{class_session} {classroom in snapshot_classroom}")
            if classroom in snapshot_classroom or teacher in snapshot_teacher or (snapshot_course_type.count("必修") > 0 or (course_type == "必修" and len(snapshot_course_type) > 0)):
                return True
        return False
    

"""
now  course_list 
必修    必修       no
必修    選修    no
選修    必修    no
選修    選修    ok
"""