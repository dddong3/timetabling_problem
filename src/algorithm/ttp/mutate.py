import random

from ..genetic_algo.mutate import Mutate
from ..genetic_algo.mutate import StrategyRegistry as MutateStrategyRegistry
from ..genetic_algo.parameter import GeneticAlgoParameter
from .chromosome import Chromosome
from ..services.custom_rule import CustomRuleService

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

custom_rule_service = CustomRuleService()

def check_classroom_with_curriculum(curriculum_class_size: int, curriculum_class_type: str, classroom: "Classroom") -> bool:
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
all_classrooms = list(set(school_curriculum_service.classrooms)) #notice Classroom  can't be change
all_session = [f'{week}/{session}' for week in range(1, 6) for session in SESSION_TABLE]
all_session = list(filter(lambda x: int(x.split('/')[1]) != 20, all_session))
all_session = sorted(all_session, key=lambda x: SESSION_TABLE.index(int(x.split('/')[1])))
print(all_session)
RESOLVE_CONFLICT = False
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

        # conflict_record = list(filter(lambda x: x["weight"] == conflict_record[0]["weight"], conflict_record))
        conflicts = conflict_record 


        for conflict in conflicts:
            skip = False
            if custom_rule_service.check_course_key_in_rule(conflict["course_key"]):
                skip = True
            match conflict["rule"]:
                case "ConflictClassroom":
                    chromosome = self.solve_class_conflict(chromosome, conflict)

                case "ConflictTeacher":
                    if skip:
                        continue
                    chromosome = self.solve_teacher_conflict(chromosome, conflict)

                case "over_70":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case "over_09":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)
                
                case "no_20":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case "ConflictGradeCourse":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case "not_on_02_or_05":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case "no_day":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case "bi_not_in_night":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case "custom_rule":
                    if skip:
                        continue
                    chromosome = self.solve_over_70(chromosome, conflict)

                case _:
                    # if conflict["rule"][0] != 'b':
                    raise NotImplementedError(f"Conflict rule {conflict['rule']} is not implemented")
                    # raise NotImplementedError(f"Conflict rule {conflict['rule']} is not implemented")
                    # pass

        # from ..services.fitness.strategies.conflict_classroom import ConflictClass

        # conflict_class = ConflictClass()

        # result = conflict_class.evaluate(chromosome.curriculums)

        # assert result == 0, f"Conflict not resolved: {result}"
            
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
        # classroom = curriculum.classroom
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

        # week, session = curriculum.week, curriculum.session

        # for classroom in all_classrooms:
        #         if self.check_conflict(chromosome_view, classroom, teacher, int(week), int(session), curriculum.session_length, curriculum.grade, curriculum.course_type):
        #             continue
        #         chromosome.set_classroom(course_key, classroom)
        #         return chromosome
        # print(f"Cannot resolve conflict: {course_key}")

        # random.shuffle(all_session)

        for session in all_session:
            week, session = session.split('/')
            for classroom in all_classrooms:
                # classroom = random.choice(all_classrooms)
                if not self.check_conflict(chromosome_view, classroom, teacher, int(week), int(session), curriculum):#.session_length, curriculum.grade, curriculum.course_type):
                    chromosome.set_time(course_key, f'{week}/{session}')
                    chromosome.set_classroom(course_key, classroom)
                    return chromosome
        
        # for target_curriculum in chromosome.curriculums:
        #     if target_curriculum.course_key == course_key:
        #         continue

        #     if self.check_swap_conflict(chromosome, curriculum, target_curriculum):
        #         continue

        cur = random.choice(chromosome.curriculums)

        tmp_classroom = curriculum.classroom
        tmp_week = curriculum.week
        tmp_session = curriculum.session

        chromosome.set_classroom(course_key, cur.classroom)
        chromosome.set_time(course_key, f'{cur.week}/{cur.session}')

        chromosome.set_classroom(cur.course_key, tmp_classroom)
        chromosome.set_time(cur.course_key, f'{tmp_week}/{tmp_session}')


        # print(f"Cannot resolve classroom conflict: {course_key}")
        return chromosome
        # raise NotImplementedError(f"Cannot resolve conflict: {course_key}")
    
    def solve_teacher_conflict(self, chromosome: Chromosome, conflict: dict):
        course_key = conflict["course_key"]
        curriculum = chromosome.find_by_course_key(course_key)
        # classroom = curriculum.classroom
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

        # random.shuffle(all_session)

        for session in all_session:
            week, session = session.split('/')
            for classroom in all_classrooms:
                if self.check_conflict(chromosome_view, classroom, teacher, int(week), int(session), curriculum):#.session_length, curriculum.grade, curriculum.course_type):
                    continue
                chromosome.set_time(course_key, f'{week}/{session}')
                chromosome.set_classroom(course_key, classroom)
                return chromosome

            
        # print(f"Cannot resolve teacher conflict: {course_key}")
        return chromosome
    
    def solve_over_70(self, chromosome: Chromosome, conflict: dict):
        course_key = conflict["course_key"]
        curriculum = chromosome.find_by_course_key(course_key)
        # classroom = curriculum.classroom
        
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

        # random.shuffle(all_session)

        for session in all_session:
            week, session = session.split('/')
            # if curriculum.session_length == 3 and (session != 2 or session != 5 or
            # classroom = random.choice(all_classrooms)
            for classroom in all_classrooms:
                if self.check_conflict(chromosome_view, classroom, teacher, int(week), int(session), curriculum):
                    continue
                chromosome.set_time(course_key, f'{week}/{session}')
                chromosome.set_classroom(course_key, classroom)
                return chromosome
            


        # print(f"Cannot resolve conflict: {course_key}")
        return chromosome
    
    def check_conflict(self, chromosome_view, classroom, teacher, week, session, curriculum): #session_length, grade, course_type):
        session_idx = SESSION_TABLE.index(session)
        session_length = curriculum.session_length
        grade = curriculum.grade
        course_type = curriculum.course_type
        course_class = curriculum.course_class

        # if session_idx <= SESSION_TABLE.index(20) <= session_idx + session_length:
        #     return True

        if session_length == 1 and session_idx >= SESSION_TABLE.index(20):
            return True

        if session_length == 3 and not (session == 2 or session == 5 or session == 40):
            return True
        
        if session_length == 2 and not (session == 1 or session == 3 or session == 5 or session == 7):
            return True
        
        if not check_classroom_with_curriculum(curriculum.class_size, curriculum.class_type, classroom):
            return True
        
        if curriculum.course_type == "必修" and session_idx >= SESSION_TABLE.index(40):
            return True

        for s in range(session_length):
            if session_idx + s >= len(SESSION_TABLE):
                return True

            class_session = SESSION_TABLE[session_idx + s]

            if class_session == 20:
                return True
            
            chromosome_view = chromosome_view.filter_time(f'{week}/{class_session}')

            if chromosome_view.check_conflict_classroom(week, class_session, classroom):
                return True
            
            if chromosome_view.check_conflict_teacher(week, class_session, teacher):
                return True
            
            if chromosome_view.check_conflict_course_type(week, class_session, course_class, course_type, grade):
                return True

        return False

    # def check_swap_conflict(self, chromosome, curriculum, target_curriculum):
    #     session_idx = SESSION_TABLE.index(session)
    #     session_length = curriculum.session_length
    #     grade = curriculum.grade
    #     course_type = curriculum.course_type
    #     # cur_time 
    #     target_curriculum = chromosome_view.find_by_time_classroom(week, session, classroom)

    #     if target_curriculum is None:
    #         return True

    #     # if session_idx <= SESSION_TABLE.index(20) <= session_idx + session_length:
    #     #     return True

    #     if session_length == 3 and not (session == 2 or session == 5 or session == 40):
    #         return True
        
    #     if not check_classroom_with_curriculum(curriculum.class_size, curriculum.class_type, classroom):
    #         return True
        
    #     if curriculum.course_type == "必修" and session_idx >= SESSION_TABLE.index(40):
    #         return True

    #     for s in range(session_length):
    #         if session_idx + s >= len(SESSION_TABLE):
    #             return True

    #         class_session = SESSION_TABLE[session_idx + s]

    #         if class_session == 20:
    #             return True
            
    #         chromosome_view = chromosome_view.filter_time(f'{week}/{class_session}')

    #         if chromosome_view.check_conflict_classroom(week, class_session, classroom):
    #             return True
            
    #         if chromosome_view.check_conflict_teacher(week, class_session, teacher):
    #             return True
            
    #         if chromosome_view.check_conflict_course_type(week, class_session, grade, course_type):
    #             return True

    #     return False

"""
now  course_list 
必修    必修       no
必修    選修    no
選修    必修    no
選修    選修    ok
"""