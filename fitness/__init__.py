from .penalty import Penalty
from .bonus import Bonus
from typing import Any, Dict

class Fitness():
    START_WEEK, END_WEEK = 1, 5
    session_list = ['01', '02', '03', '04', '20', '05', '06', '07', '08', '09', '40', '50', '60', '70']

    def __init__(self):
        self.penalty = Penalty(self.session_list)
        self.bonus = Bonus(self.session_list)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.compute_fitness(*args, **kwds)

    def compute_fitness(self, chromosome: list[dict]) -> int:
        teacher_class_week = {}
        course_week = {}
        fitness = [dict(), dict()] # [penalty, bonus]

        for gene in chromosome:
            for teacher in gene['teacher_list']:
                if teacher not in teacher_class_week:
                    teacher_class_week[teacher] = {}
                    for week in range(self.START_WEEK, self.END_WEEK + 1):
                        teacher_class_week[teacher][week] = {}
                teacher_session = teacher_class_week[teacher][gene['week']].get(gene['session'], 0)
                teacher_class_week[teacher][gene['week']][gene['session']] = teacher_session + 1

            if gene['course_id'] not in course_week:
                course_week[gene['course_id']] = {}
                for week in range(self.START_WEEK, self.END_WEEK + 1):
                    course_week[gene['course_id']][str(week)] = {}
            course_session = course_week[gene['course_id']][str(gene['week'])].get(gene['session'], 0)
            course_week[gene['course_id']][str(gene['week'])][gene['session']] = course_session + 1

            fitness[0][2] = self.penalty.rule_2(gene)
            fitness[0][4] = self.penalty.rule_4(gene)

        for teacher in teacher_class_week:
            fitness[0][3] = self.penalty.rule_3(teacher_class_week[teacher])
            fitness[0][6] = self.penalty.rule_6(teacher_class_week[teacher])

        for course in course_week:
            # print(course_week)
            lst = self.evaluate_course_week(course_week[course])
            fitness[0][1] = lst[0]
            fitness[1][1] = lst[1]

        return fitness

    def evaluate_course_week(self, course_week: dict) -> list[int]:
        course_week_total = 0
        is_3_session = False
        session_start_25 = False

        for week in course_week:
            course_week_total += sum(course_week[week].values())

            if len(course_week[week]) == 3:
                session_index = [self.session_list.index(_) for _ in course_week[week]]
                min_index = min(session_index)
                is_3_session = sum(session_index) - 3 * min_index == 3
                session_start_25 |= min_index == self.session_list.index('02') or min_index == self.session_list.index('05')

        #[penalty, bonus]
        fitness_list = [self.penalty.rule_1(course_week_total, is_3_session), self.bonus.rule_1(course_week_total, is_3_session, session_start_25)]
        return fitness_list
